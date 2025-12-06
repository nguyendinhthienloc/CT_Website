# Vietnam POI Finder 🗺️

A web application that allows users to search for locations in Vietnam and displays 5 nearby points of interest on an interactive map.

## Features

✨ **Key Features:**
- 🔍 Search locations in Vietnam (cities, districts, streets, landmarks...)
- 🗺️ Display locations on an interactive map (Leaflet + OpenStreetMap)
- 📍 Automatically find and display 5 nearby points of interest:
  - Tourist attractions (tourism)
  - Restaurants and cafes (amenity)
  - Historical sites (historic)
- 💡 Beautiful, responsive UI with Tailwind CSS
- 🎯 Click on points of interest to view details on the map

## Technologies Used

- **Leaflet.js** - Interactive map library
- **OpenStreetMap** - Map data and tiles
- **Nominatim API** - Geocoding (convert location names to coordinates)
- **Overpass API** - Search for Points of Interest from OpenStreetMap
- **Tailwind CSS** - Styling framework

## How to Run

### Method 1: Using Python HTTP Server

```bash
# Open terminal in the project directory
cd /workspaces/CT_Week5_24125093

# Run the server (Python 3)
python3 -m http.server 8001

# Open your browser and visit:
# http://localhost:8001/index.html
```
<!-- Optional: you may use any static server, but the repo expects frontend on port 8001 -->

### Backend (optional, recommended for production)

This project includes a small Python backend proxy (FastAPI) that can be used to:
- Proxy weather requests to OpenWeatherMap so you don't expose the API key client-side
- Proxy translation requests to public LibreTranslate/Argos endpoints (adds CORS and fallback handling)

Files:
- `backend/main.py` - FastAPI app with `/api/weather` and `/api/translate`
- `backend/requirements.txt` - Python dependencies
- `backend/.env.example` - example environment variables

To run the backend locally:

```bash
# 1) Create a virtualenv (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r backend/requirements.txt

# 3) Copy and set your env vars
cp backend/.env.example backend/.env
# Edit backend/.env and set OPENWEATHERMAP_KEY (register at https://openweathermap.org/ if you don't have one)

# 4) Run the app with uvicorn (listens on :8000 for this project)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Client changes (optional):
- If you run the backend locally, the client is already configured to call the backend API base at `http://localhost:8000` for `/api/*` endpoints. Do not expose OpenWeatherMap API keys to the browser.

Registration notes (manual work):
- OpenWeatherMap: create a free account and generate an API key at https://openweathermap.org/ — required to use the `/api/weather` endpoint.
- LibreTranslate / Argos: public endpoints used by `/api/translate` are free and do not require keys, but public instances may rate-limit or impose CORS restrictions; if you need reliable translation, consider a self-hosted LibreTranslate or a paid translation API.

Translation library (py-googletrans):
- This backend can optionally use `py-googletrans` (`googletrans` package) for server-side translation without API keys. That library is included in `backend/requirements.txt` as `googletrans==3.1.0a0`.
- `py-googletrans` is an unofficial wrapper and may break if Google changes their internal API. It is a good no-key option for development and light usage.
- If `googletrans` is available, the backend will use it automatically for `/api/translate`. If it's not available or fails, the backend falls back to public LibreTranslate/Argos endpoints.

No registration is required to use `py-googletrans`. For production-grade translation, consider a paid API (Google Cloud Translate, Azure Translator) and proxy the requests server-side with proper key management.


### Method 3: Open File Directly

You can also open the `index.html` file directly in your browser (double-click), but using an HTTP server is recommended to avoid CORS errors.

## User Guide

1. **Enter a location name** in the search box (e.g., "Hanoi", "Da Nang", "Hoi An", "Nha Trang")
2. **Click the "🔍 Search" button** or press Enter
3. **Wait for the app** to search and display:
   - Main location on the map (red marker 📍)
   - 5 nearby points of interest (blue markers with numbers)
   - List of points of interest above the map
4. **Click on a POI card** to view details on the map

## Example Searches

You can try these locations:
- Hanoi (Hà Nội)
- Hoi An (Hội An)
- Da Nang (Đà Nẵng)
- Nha Trang
- Saigon / Ho Chi Minh City (Sài Gòn)
- Hanoi Old Quarter (Phố cổ Hà Nội)
- My Khe Beach (Bãi biển Mỹ Khê)
- One Pillar Pagoda (Chùa Một Cột)
- Soc Trang (Sóc Trăng)

## Project Structure

```
CT_Week5_24125093/
├── index.html          # Main application (HTML + CSS + JavaScript)
├── main.html           # Old Firebase demo
├── README.md           # This documentation
└── IMPROVEMENTS.md     # Detailed list of improvements made
```

## APIs Used

### 1. Nominatim API (Geocoding)
- URL: `https://nominatim.openstreetmap.org/search`
- Function: Convert location name → coordinates (lat, lon)
- Free, no API key required

### 2. Overpass API (POI Search)
- URL: `https://overpass-api.de/api/interpreter`
- Function: Find points of interest within 3km radius
- Free, no API key required

## Notes

- ✅ Completely free application, no API key registration needed
- ✅ Works after initial load (except for API calls)
- ⚠️ Nominatim has a rate limit: 1 request/second - sufficient for normal use
- ⚠️ Results depend on OpenStreetMap data (may not be complete in some areas)

## Troubleshooting

If you don't see results:
1. Try a more specific location name (e.g., "Hanoi" instead of "HN")
2. Try a larger location (city instead of small street)
3. Check your internet connection
4. Some areas may have limited POI data on OpenStreetMap
5. Press `Ctrl+Shift+D` to open the debug panel and see what's happening

## Features & Improvements

- ✨ Quick search buttons for popular destinations
- 🎯 Search result caching for instant repeated searches
- 🔄 Multiple fallback strategies ensure results
- 📱 Fully responsive design
- 🐛 Comprehensive error handling
- 💡 Debug panel (Ctrl+Shift+D) for troubleshooting

## Author

CT Week 5 Project - Student ID: 24125093

## License

MIT License - Free to use for educational and personal purposes.

## Quick Two-Terminal Run (recommended)

Run the project locally using two terminals:

Terminal A — Backend

1. Create virtual environment and install deps
  ```bash
  python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt
  ```
2. Export env var(s):
  ```bash
  export OPENWEATHERMAP_KEY=YOUR_KEY
  ```
3. Start backend:
  ```bash
  python backend/main.py
  # or:
  uvicorn backend.main:app --host 0.0.0.0 --port 8000
  ```

Terminal B — Frontend

1. Serve static files from project root:
  ```bash
  python -m http.server 8001
  ```
2. Open browser at:
  ```
  http://localhost:8001/index.html
  ```

Notes:

* Backend API base URL: http://localhost:8000
* Frontend static server: http://localhost:8001
