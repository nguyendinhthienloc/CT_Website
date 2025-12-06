# 🧪 Simple Testing Steps

## 🚀 How to Test the Login Screen

### Step 1: Open the Application
1. Make sure the server is running: `python3 -m http.server 8080`
2. Open in browser: **http://localhost:8080/index.html**

---

## ✅ What You Should See

### **IMMEDIATELY on page load:**

```
┌─────────────────────────────────────┐
│                                     │
│            🗺️                       │
│      Khám Phá Việt Nam              │
│                                     │
│   Đăng nhập để khám phá các điểm   │
│   du lịch tuyệt vời và lưu địa     │
│   điểm yêu thích của bạn           │
│                                     │
│   ┌──────────────────────────┐    │
│   │ 🔐 Đăng nhập với Google  │    │
│   └──────────────────────────┘    │
│                                     │
│   ✅ Lưu địa điểm yêu thích        │
│   🗺️ Khám phá 5 điểm thú vị        │
│   🌤️ Xem thời tiết địa phương      │
│                                     │
└─────────────────────────────────────┘
```

**Behind the login screen:** Blurred content (map, search, etc.)

---

## 📝 Testing Sequence

### ✅ Test 1: Login Screen Appears First
- [ ] Login screen is visible (purple gradient background)
- [ ] Main content is blurred in background
- [ ] Cannot interact with map or search features
- [ ] "Đăng nhập với Google" button is visible

---

### ✅ Test 2: Click Login Button

**Action:** Click "🔐 Đăng nhập với Google"

**Expected:**
- [ ] Button text changes to "⏳ Đang đăng nhập..."
- [ ] Google Sign-In popup window opens
- [ ] Can see your Google accounts

**Note:** If popup is blocked, allow popups for localhost

---

### ✅ Test 3: Complete Google Login

**Action:** Select your Google account and authorize

**Expected:**
- [ ] Popup closes automatically
- [ ] Login screen **fades out** (disappears)
- [ ] Main content **un-blurs** and becomes interactive
- [ ] User profile appears in header (top-right)
  - Shows your avatar
  - Shows your name
  - Shows "Thoát" (logout) button
- [ ] Green success message: "✅ Đã đăng nhập!"
- [ ] Favorites section appears (empty at first)

**Browser Console should show:**
```
✅ Đăng nhập thành công!
👤 User logged in: [Your Name]
```

---

### ✅ Test 4: Use Main Features (Now Accessible)

**Action:** Search for "Hà Nội"

**Expected:**
- [ ] Search works normally
- [ ] Map shows Hà Nội
- [ ] Weather information displays
- [ ] 5 Points of Interest (POI) appear
- [ ] Each POI has "💾 Lưu" button

---

### ✅ Test 5: Save a Favorite

**Action:** Click "💾 Lưu" on any POI

**Expected:**
- [ ] Notification appears: "⭐ Đã lưu vào yêu thích!"
- [ ] Notification bounces and disappears after 2 seconds
- [ ] Favorites section shows the saved place
- [ ] Saved place has amber/orange background

---

### ✅ Test 6: Logout

**Action:** Click "Thoát" button in user profile

**Expected:**
- [ ] Confirmation: "Bạn có chắc muốn đăng xuất?"
- [ ] Click OK
- [ ] Login screen **appears again** (purple background)
- [ ] Main content **blurs** again
- [ ] Cannot interact with features
- [ ] Favorites section hidden
- [ ] Back to starting state

---

## 🔍 Troubleshooting

### Problem: Login screen doesn't appear
**Solution:** 
- Check browser console (F12) for errors
- Refresh the page (Ctrl+R or Cmd+R)
- Clear cache and reload (Ctrl+Shift+R)

### Problem: Google popup doesn't open
**Solution:**
- Allow popups for localhost in browser settings
- Try Chrome/Edge instead of Firefox
- Check if logged into Google account

### Problem: Stuck at "Đang đăng nhập..."
**Solution:**
- Close the Google popup if stuck
- Refresh the page
- Check internet connection
- Check Firebase Console for authorization issues

### Problem: Can see content without logging in
**Solution:**
- Hard refresh: Ctrl+Shift+R
- Clear browser cache
- Check if JavaScript is enabled

---

## 🎯 Quick Test Checklist

```
[ ] 1. Open page → Login screen shows first ✓
[ ] 2. Click login → Google popup opens ✓
[ ] 3. Authorize → Login screen disappears ✓
[ ] 4. Profile shows → Can use all features ✓
[ ] 5. Save place → Appears in favorites ✓
[ ] 6. Logout → Login screen appears again ✓
```

---

## 🌐 Expected URLs

- **Application:** http://localhost:8080/index.html
- **Server must be running on port 8080**

---

## 📸 Visual Flow

```
START
  ↓
[Login Screen] 🔐
  ↓ (Click login)
[Google Popup] 🪟
  ↓ (Authorize)
[Main App] 🗺️ (Favorites, Search, Map)
  ↓ (Click logout)
[Login Screen] 🔐 (Back to start)
```

---

**Ready to test!** 🚀

Just open http://localhost:8080/index.html and follow the steps above.
