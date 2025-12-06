# ✅ All Services Running!

## 🚀 Active Services

### 1. **Frontend (Main App)**
- **URL:** http://localhost:8080/index.html
- **Status:** ✅ Running
- **Purpose:** Your travel search application with Firebase auth

### 2. **FastAPI Backend (Port 8001)**
- **URL:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs
- **Status:** ✅ Running
- **Purpose:** Provides:
  - `/api/geocode` - Location search
  - `/api/poi` - Points of interest
  - `/api/weather` - Weather data
  - `/api/translate` - Translation (LibreTranslate)

### 3. **Flask Backend (Port 5001)**
- **URL:** http://localhost:5001
- **Status:** ✅ Running  
- **Purpose:** Provides:
  - `/translate` - Google Translate API

---

## 🔐 Firebase Setup (Required)

### **Add Authorized Domain:**

1. Go to: **https://console.firebase.google.com**
2. Select your project: **ct-week5-24125093**
3. Go to **Authentication** → **Settings** tab
4. Scroll to **Authorized domains**
5. Click **Add domain**
6. Add your domain:
   - For Codespaces: `your-codespace-name.preview.app.github.dev`
   - For local: `localhost` (should already be there)
   - For deployment: Your actual domain

**To find your Codespaces domain:**
- Look at the URL when you open the Simple Browser
- It will be something like: `https://xxxx-8080.app.github.dev`
- Add just the domain part: `xxxx.app.github.dev`

---

## 🧪 Test Everything

### **Step 1: Test Login**
1. Open: http://localhost:8080/index.html
2. You should see the purple login screen
3. Click "🔐 Đăng nhập với Google"
4. Login with your Google account
5. ✅ Login screen disappears, you're in!

### **Step 2: Test Search (requires backend)**
1. After logging in, search for: **Hà Nội**
2. Wait a few seconds
3. ✅ Should see:
   - Map centered on Hà Nội
   - Weather information (temperature, etc.)
   - 5 points of interest (POIs)

### **Step 3: Test Translation**
1. Scroll to "Dịch nhanh (EN → VI)" section
2. Type: **"Hello, how are you?"**
3. Click "Dịch → VN"
4. ✅ Should see: "Xin chào, bạn khỏe không?"

### **Step 4: Test Favorites**
1. After searching for a location
2. Click "💾 Lưu" on any POI
3. ✅ Should see:
   - Success notification: "⭐ Đã lưu vào yêu thích!"
   - Place appears in Favorites section

---

## 🐛 Troubleshooting

### **Login doesn't work:**
```
❌ Problem: "Unauthorized domain" error
✅ Solution: Add authorized domain in Firebase Console (see above)
```

### **Search/Weather doesn't work:**
```
❌ Problem: No results or errors
✅ Solution: Check if FastAPI backend is running
   Test: curl http://localhost:8001
   Restart: cd backend && uvicorn main:app --port 8001
```

### **Translation doesn't work:**
```
❌ Problem: "Lỗi dịch" error
✅ Solution: Check if Flask backend is running
   Test: curl http://localhost:5001
   Restart: cd backend && python3 app.py
```

### **Check backend logs:**
```bash
# FastAPI logs
tail -f /workspaces/CT_Week5_24125093/backend/fastapi.log

# Flask logs
tail -f /workspaces/CT_Week5_24125093/backend/flask.log
```

---

## 📊 Service Status Check

Run this command to check all services:
```bash
echo "Frontend: http://localhost:8080" && \
curl -s http://localhost:8080 > /dev/null && echo "✅ Running" || echo "❌ Down" && \
echo -e "\nFastAPI: http://localhost:8001" && \
curl -s http://localhost:8001/docs > /dev/null && echo "✅ Running" || echo "❌ Down" && \
echo -e "\nFlask: http://localhost:5001" && \
curl -s http://localhost:5001 > /dev/null && echo "✅ Running" || echo "❌ Down"
```

---

## 🔄 Restart Services

If something stops working:

```bash
# Kill all services
pkill -f "python3 -m http.server"
pkill -f "uvicorn"
pkill -f "python3 app.py"

# Restart everything
cd /workspaces/CT_Week5_24125093
python3 -m http.server 8080 &
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 &
python3 app.py &
```

---

## 🎯 Quick Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Main App** | http://localhost:8080/index.html | Your application |
| **FastAPI Docs** | http://localhost:8001/docs | API documentation |
| **Flask Status** | http://localhost:5001 | Translation service |

---

**All systems ready!** 🚀 

Just make sure to add the authorized domain in Firebase Console, then you're good to go!
