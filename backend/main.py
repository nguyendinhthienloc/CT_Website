from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gradio_client import Client
import time
from datetime import datetime

import requests

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
