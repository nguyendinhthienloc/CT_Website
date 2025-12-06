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

### 🚀 Quick Start (Frontend Only)

The simplest way to run the application without backend features:

```bash
# Navigate to project directory
cd /workspaces/CT_Week5_24125093

# Start a local web server
python3 -m http.server 8001

# Open your browser and visit:
# http://localhost:8001/frontend/index.html
```

**What works:**
- ✅ Location search and mapping
- ✅ Points of interest discovery
- ✅ Interactive map features
- ✅ All core functionality

**What's disabled:**
- ❌ Weather information (requires backend)
- ❌ Translation features (requires backend)

### 🔥 Full Stack Setup (Frontend + Backend)

For complete functionality including weather and translation features, run both frontend and backend:

**Terminal 1 - Backend Setup:**

```bash
# 1. Navigate to project directory
cd /workspaces/CT_Week5_24125093

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r backend/requirements.txt

# 4. Set up environment variables (optional but recommended)
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENWEATHERMAP_KEY
# Get a free key at: https://openweathermap.org/

# 5. Start the backend server
python backend/main.py
# Backend will run on http://localhost:8000
```

**Terminal 2 - Frontend Setup:**

```bash
# 1. Navigate to project directory
cd /workspaces/CT_Week5_24125093

# 2. Start the frontend server
python3 -m http.server 8001

# 3. Open browser to:
# http://localhost:8001/frontend/index.html
```

**Backend Features:**
- 🌤️ Weather API proxy (`/api/weather`) - Requires OpenWeatherMap API key
- 🌍 Translation API (`/api/translate`) - Uses py-googletrans (no key needed)
- 🔒 Secure API key handling (keys stay on server)

**API Endpoints:**
- `GET /api/weather?lat={lat}&lon={lon}` - Get weather for coordinates
- `POST /api/translate` - Translate text (body: `{text, dest}`)

### 📁 Alternative: Direct File Access

Open `frontend/index.html` directly in your browser, but note:
- ⚠️ May have CORS issues with some APIs
- ⚠️ Backend features won't work
- ✅ Use HTTP server method for best experience

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
├── frontend/
│   ├── index.html           # Main application (HTML + CSS + JavaScript)
│   ├── pages/
│   │   ├── main.html        # Firebase authentication demo
│   │   └── test.html        # Backend connectivity test
│   └── assets/              # Static assets (images, styles, etc.)
├── backend/
│   ├── main.py              # FastAPI application
│   ├── app.py               # Flask application (legacy)
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── setup_env.sh         # Environment setup script
├── docs/
│   ├── FIREBASE_AUTH_GUIDE.md
│   ├── IMPROVEMENTS.md
│   ├── RUNNING.md
│   ├── SERVICES_RUNNING.md
│   ├── TEST_CHECKLIST.md
│   ├── TESTING_STEPS.md
│   └── Using py-googletrans for Translation.txt
├── documents/               # Jupyter notebooks and lab materials
└── README.md                # This documentation
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

## 🐳 Running in Development Containers / Codespaces

This project is configured for GitHub Codespaces and VS Code Dev Containers:

```bash
# The environment is already set up, just run:

# Terminal 1 - Backend
source .venv/bin/activate  # Virtual environment should exist
python backend/main.py

# Terminal 2 - Frontend  
python3 -m http.server 8001

# Access via forwarded ports or direct URLs
```

**Port Configuration:**
- `8000` - Backend API (FastAPI)
- `8001` - Frontend static server
- `5001` - Flask legacy server (optional)

## 📚 Additional Documentation

For more detailed information, see the `docs/` directory:
- `docs/RUNNING.md` - Detailed running instructions
- `docs/FIREBASE_AUTH_GUIDE.md` - Firebase authentication setup
- `docs/IMPROVEMENTS.md` - Feature improvements log
- `docs/TESTING_STEPS.md` - Testing procedures
- `docs/SERVICES_RUNNING.md` - Service management guide
