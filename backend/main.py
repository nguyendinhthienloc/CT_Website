from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Vietnam POI Helper API")

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
    if not OPENWEATHER_KEY:
        raise HTTPException(status_code=500, detail="Server missing OPENWEATHERMAP_KEY environment variable")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={payload.lat}&lon={payload.lon}"
        f"&appid={OPENWEATHER_KEY}&units=metric"
    )

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail={"upstream_status": resp.status_code, "body": resp.text})

    return resp.json()


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
    url = (
        f"https://nominatim.openstreetmap.org/search?q={httpx.utils.quote(payload.q)}&format=json&limit={payload.limit}&addressdetails=1"
    )

    headers = {"User-Agent": "VietnamPOIFinder/1.0"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail={"upstream_status": resp.status_code, "body": resp.text})

    try:
        return resp.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Invalid JSON from geocode service")


@app.post("/api/poi")
async def proxy_poi(payload: PoiRequest):
    """Proxy Overpass POI search and fallback to Nominatim categories when empty."""
    radius = payload.radius
    lat = payload.lat
    lon = payload.lon

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
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(overpass_url, data={'data': overpass_query}, headers={"Content-Type": "application/x-www-form-urlencoded"})
        except Exception as e:
            r = None

    if r and r.status_code == 200:
        try:
            j = r.json()
            elements = j.get('elements', [])
            if elements:
                return {"elements": elements}
        except Exception:
            pass

    # Fallback: use Nominatim nearby searches for common categories
    categories = ['restaurant', 'cafe', 'museum', 'park', 'hotel', 'shop']
    results = []
    headers = {"User-Agent": "VietnamPOIFinder/1.0"}

    async with httpx.AsyncClient(timeout=15.0) as client:
        for category in categories:
            if len(results) >= 5:
                break
            try:
                search_url = f"https://nominatim.openstreetmap.org/search?q={httpx.utils.quote(category)}+near+{lat},{lon}&format=json&limit=3"
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
