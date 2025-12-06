from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
import urllib.parse
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Vietnam POI Helper API")

# Activity logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{'='*80}")
    print(f"[{timestamp}] 📥 INCOMING REQUEST")
    print(f"Method: {request.method}")
    print(f"Path: {request.url.path}")
    print(f"Client: {request.client.host if request.client else 'unknown'}")
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        print(f"Status: {response.status_code}")
        print(f"Duration: {duration:.3f}s")
        print(f"✅ REQUEST COMPLETED")
        print(f"{'='*80}\n")
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ ERROR: {str(e)}")
        print(f"Duration: {duration:.3f}s")
        print(f"{'='*80}\n")
        raise

# Allow local origins - adjust in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENWEATHER_KEY = os.getenv("OPENWEATHERMAP_KEY")


class WeatherRequest(BaseModel):
    lat: float
    lon: float


class TranslateRequest(BaseModel):
    q: str
    source: str = "en"
    target: str = "vi"


class GeocodeRequest(BaseModel):
    q: str
    limit: int = 1


class PoiRequest(BaseModel):
    lat: float
    lon: float
    radius: int = 3000


@app.post("/api/weather")
async def proxy_weather(payload: WeatherRequest):
    """Proxy weather requests to OpenWeatherMap. Requires OPENWEATHERMAP_KEY in env."""
    print(f"🌤️  Weather request for: lat={payload.lat}, lon={payload.lon}")
    
    if not OPENWEATHER_KEY:
        print("❌ Missing OPENWEATHERMAP_KEY")
        raise HTTPException(status_code=500, detail="Server missing OPENWEATHERMAP_KEY environment variable")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={payload.lat}&lon={payload.lon}"
        f"&appid={OPENWEATHER_KEY}&units=metric"
    )

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url)

        if resp.status_code != 200:
            print(f"❌ Weather API error: {resp.status_code}")
            raise HTTPException(status_code=502, detail={"upstream_status": resp.status_code, "body": resp.text})

        print(f"✅ Weather data retrieved successfully")
        return resp.json()
    except httpx.TimeoutException:
        print("❌ Weather API timeout")
        raise HTTPException(status_code=504, detail="Weather service timeout")
    except Exception as e:
        print(f"❌ Weather API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Weather service error: {str(e)}")


@app.post("/api/translate")
async def proxy_translate(payload: TranslateRequest):
    """Proxy translation requests to public LibreTranslate / Argos endpoints with simple fallback."""
    endpoints = [
        "https://translate.argosopentech.com/translate",
        "https://libretranslate.com/translate",
    ]

    data = {"q": payload.q, "source": payload.source, "target": payload.target, "format": "text"}

    async with httpx.AsyncClient(timeout=15.0) as client:
        for url in endpoints:
            try:
                r = await client.post(url, json=data)
            except Exception as e:
                # try next
                last_err = str(e)
                continue

            if r.status_code == 200:
                try:
                    j = r.json()
                    # standardize response
                    return {"translatedText": j.get("translatedText") or j.get("result")}
                except Exception:
                    raise HTTPException(status_code=502, detail="Invalid JSON from translation service")

            # if 400, return the upstream message to help debugging
            last_err = f"{r.status_code} {r.text}"

    raise HTTPException(status_code=502, detail={"error": "All translation endpoints failed", "detail": last_err})


@app.post("/api/geocode")
async def proxy_geocode(payload: GeocodeRequest):
    """Proxy Nominatim geocoding requests."""
    print(f"📍 Geocode request for: '{payload.q}' (limit: {payload.limit})")
    
    url = (
        f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(payload.q)}&format=json&limit={payload.limit}&addressdetails=1"
    )

    headers = {"User-Agent": "VietnamPOIFinder/1.0"}
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=headers)

        if resp.status_code != 200:
            print(f"❌ Geocode API error: {resp.status_code}")
            raise HTTPException(status_code=502, detail={"upstream_status": resp.status_code, "body": resp.text})

        result = resp.json()
        print(f"✅ Found {len(result)} location(s)")
        return result
    except httpx.TimeoutException:
        print("❌ Geocode API timeout")
        raise HTTPException(status_code=504, detail="Geocode service timeout")
    except Exception as e:
        print(f"❌ Geocode error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Geocode service error: {str(e)}")


@app.post("/api/poi")
async def proxy_poi(payload: PoiRequest):
    """Proxy Overpass POI search and fallback to Nominatim categories when empty."""
    radius = payload.radius
    lat = payload.lat
    lon = payload.lon
    
    print(f"🗺️  POI request: lat={lat}, lon={lon}, radius={radius}m")

    overpass_query = f"""
      [out:json][timeout:25];
      (
        node["name"](around:{radius},{lat},{lon});
        way["name"](around:{radius},{lat},{lon});
      );
      out body 50;
      >;
      out skel qt;
    """

    overpass_url = 'https://overpass-api.de/api/interpreter'
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(overpass_url, data={'data': overpass_query}, headers={"Content-Type": "application/x-www-form-urlencoded"})
        
        if r.status_code == 200:
            j = r.json()
            elements = j.get('elements', [])
            if elements:
                print(f"✅ Found {len(elements)} POIs from Overpass")
                return {"elements": elements}
    except Exception as e:
        print(f"⚠️  Overpass API failed: {str(e)}, trying fallback...")

    # Fallback: use Nominatim nearby searches for common categories
    categories = ['restaurant', 'cafe', 'museum', 'park', 'hotel', 'shop']
    results = []
    headers = {"User-Agent": "VietnamPOIFinder/1.0"}

    async with httpx.AsyncClient(timeout=15.0) as client:
        for category in categories:
            if len(results) >= 5:
                break
            try:
                search_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(category)}+near+{lat},{lon}&format=json&limit=3"
                resp = await client.get(search_url, headers=headers)
                if resp.status_code != 200:
                    continue
                places = resp.json()
                for place in places:
                    if len(results) >= 5:
                        break
                    if place.get('lat') and place.get('lon') and place.get('display_name'):
                        results.append({
                            'name': place.get('display_name').split(',')[0],
                            'type': category.capitalize(),
                            'lat': float(place.get('lat')),
                            'lon': float(place.get('lon')),
                            'description': place.get('display_name')
                        })
            except Exception:
                continue

    # Always include center location as first
    center = {'name': 'Center', 'type': 'Search center', 'lat': lat, 'lon': lon, 'description': 'Search center location'}
    pois = [center] + results[:4]
    return {"fallback": True, "pois": pois}


@app.get("/")
async def root():
    return {"status": "ok", "note": "This is the backend proxy for weather and translation."}
