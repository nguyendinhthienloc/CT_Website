from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gradio_client import Client
import time
from datetime import datetime

import requests
import os

app = FastAPI(title="Website Backend API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Logging ----------
@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{ts}] {request.method} {request.url.path}")
    response = await call_next(request)
    duration = time.time() - start
    print(f"STATUS {response.status_code} ({duration:.3f}s)")
    return response

# ---------- Models ----------
class HFRequest(BaseModel):
    inputs: str

class TranslateRequest(BaseModel):
    q: str
    source: str = "en"
    target: str = "vi"


class GeocodeRequest(BaseModel):
    q: str
    limit: int = 1


class POIRequest(BaseModel):
    lat: float
    lon: float
    radius: int = 3000


class WeatherRequest(BaseModel):
    lat: float
    lon: float

# ---------- Hugging Face (via Space) ----------
# Use a single shared Gradio Client instance for the Space
HF_SPACE_ID = "locnguyen0304/hf-sentiment-api"
hf_client = Client(HF_SPACE_ID)

@app.post("/api/hf")
def hf_proxy(payload: HFRequest):
    """
    Hugging Face-backed AI feature (sentiment analysis).
    Uses a Hugging Face Space as the backend.
    """
    try:
        result = hf_client.predict(
            payload.inputs,
            api_name="/predict"
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Hugging Face Space error: {str(e)}"
        )

# ---------- Translation (direct public APIs) ----------
@app.post("/api/translate")
def translate(payload: TranslateRequest):
    data = {
        "q": payload.q,
        "source": payload.source,
        "target": payload.target,
        "format": "text"
    }

    endpoints = [
        "https://translate.argosopentech.com/translate",
        "https://libretranslate.com/translate",
    ]

    for url in endpoints:
        try:
            r = requests.post(url, json=data, timeout=10)
            if r.status_code == 200:
                j = r.json()
                return {"translatedText": j.get("translatedText")}
        except Exception:
            continue

    raise HTTPException(status_code=502, detail="All translation services failed")

# ---------- Health ----------
@app.get("/")
def root():
    return {
        "status": "ok",
        "note": "FastAPI backend with Hugging Face integration"
    }


# ---------- Geocoding (Nominatim) ----------
@app.post("/api/geocode")
def geocode(payload: GeocodeRequest):
    try:
        params = {
            "q": payload.q,
            "format": "json",
            "limit": payload.limit,
        }
        headers = {"User-Agent": "ct-week5-geocoder/1.0"}
        r = requests.get("https://nominatim.openstreetmap.org/search", params=params, headers=headers, timeout=10)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Geocoding service error")
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


# ---------- Points of Interest (Overpass) ----------
@app.post("/api/poi")
def poi(payload: POIRequest):
    try:
        # Construct Overpass QL query to get nodes/ways/relations with common POI tags
        query = f"""
[out:json][timeout:25];
(
  node(around:{payload.radius},{payload.lat},{payload.lon})[tourism];
  node(around:{payload.radius},{payload.lat},{payload.lon})[amenity];
  node(around:{payload.radius},{payload.lat},{payload.lon})[historic];
  way(around:{payload.radius},{payload.lat},{payload.lon})[tourism];
  way(around:{payload.radius},{payload.lat},{payload.lon})[amenity];
  relation(around:{payload.radius},{payload.lat},{payload.lon})[tourism];
);
out center 50;
"""

        r = requests.post("https://overpass-api.de/api/interpreter", data={"data": query}, timeout=30)
        if r.status_code == 200:
            return r.json()

        # If Overpass fails, return a small fallback list
        fallback_pois = [
            {"name": "Điểm tham quan mẫu", "type": "Tourism", "lat": payload.lat + 0.002, "lon": payload.lon + 0.002, "icon": "⭐", "description": "Điểm tham quan mẫu"},
            {"name": "Nhà hàng mẫu", "type": "Restaurant", "lat": payload.lat - 0.002, "lon": payload.lon - 0.002, "icon": "🍽️", "description": "Nhà hàng địa phương"}
        ]

        return {"fallback": True, "pois": fallback_pois}
    except Exception as e:
        # Return fallback on error
        fallback_pois = [
            {"name": "Điểm tham quan mẫu", "type": "Tourism", "lat": payload.lat + 0.002, "lon": payload.lon + 0.002, "icon": "⭐", "description": "Điểm tham quan mẫu"}
        ]
        return {"fallback": True, "pois": fallback_pois}


# ---------- Weather (OpenWeatherMap proxy) ----------
@app.post("/api/weather")
def weather(payload: WeatherRequest):
    key = os.getenv("OPENWEATHERMAP_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="OpenWeatherMap API key not configured")

    try:
        params = {
            "lat": payload.lat,
            "lon": payload.lon,
            "units": "metric",
            "appid": key
        }
        r = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Weather service error")
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
