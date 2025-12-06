# 🧪 Firebase Authentication Test Checklist

## ✅ Test Results - December 6, 2025

### Environment Setup
- ✅ Web server running on http://localhost:8080
- ✅ index.html loaded successfully
- ✅ No HTML syntax errors detected

---

## 📋 Manual Testing Steps

### 1️⃣ Initial Page Load
**Test**: Open http://localhost:8080/index.html

**Expected Results:**
- [ ] Page loads without errors
- [ ] "🔐 Đăng nhập Google" button is visible in the header
- [ ] Auth hint shows: "💡 Đăng nhập để lưu các địa điểm yêu thích của bạn!"
- [ ] Favorites section is hidden (not logged in)
- [ ] All other sections (translator, search, map) work normally

**Check Browser Console:**
```
Should see: Firebase SDKs loading messages (no errors)
```

---

### 2️⃣ Google Sign-In
**Test**: Click the "🔐 Đăng nhập Google" button

**Expected Results:**
- [ ] Google Sign-In popup window appears
- [ ] Can select/authorize with Google account
- [ ] After authorization, popup closes
- [ ] User profile appears in top-right with avatar and name
- [ ] Login button disappears
- [ ] Auth hint changes to: "✅ Đã đăng nhập! Bạn có thể lưu địa điểm yêu thích."
- [ ] Favorites section becomes visible (may show empty state)

**Browser Console:**
```
Should see: "✅ Đăng nhập thành công!"
Should see: "👤 User logged in: [Your Name]"
```

---

### 3️⃣ Search for Places
**Test**: Search for "Hà Nội" or "Đà Nẵng"

**Expected Results:**
- [ ] Location search works as before
- [ ] Map centers on the location
- [ ] Weather information displays
- [ ] 5 Points of Interest (POIs) appear
- [ ] Each POI card now has TWO buttons:
  - [ ] "🗺️ Xem trên bản đồ" (blue button)
  - [ ] "💾 Lưu" (amber/orange gradient button)

---

### 4️⃣ Save Favorite Place
**Test**: Click "💾 Lưu" on any POI card

**Expected Results:**
- [ ] Success notification appears: "⭐ Đã lưu vào yêu thích!"
- [ ] Notification bounces and disappears after 2 seconds
- [ ] Favorites section updates automatically
- [ ] Saved place appears in favorites section with:
  - [ ] Amber/orange gradient background
  - [ ] Place name, type, and icon
  - [ ] Save date
  - [ ] "🗺️ Xem trên bản đồ" button
  - [ ] "❌" remove button

**Browser Console:**
```
Should see: "✅ Đã lưu yêu thích: [Place Name]"
```

---

### 5️⃣ View Favorite on Map
**Test**: Click "🗺️ Xem trên bản đồ" in favorites section

**Expected Results:**
- [ ] Map centers on the saved location
- [ ] Marker popup opens (if marker exists)
- [ ] Page smoothly scrolls to map section

---

### 6️⃣ Remove Favorite
**Test**: Click "❌" button on a favorite card

**Expected Results:**
- [ ] Confirmation dialog appears: "Xóa địa điểm này khỏi yêu thích?"
- [ ] Click OK to confirm
- [ ] Card disappears from favorites section
- [ ] If no favorites remain, empty state message appears

**Browser Console:**
```
Should see: "🗑️ Đã xóa yêu thích"
```

---

### 7️⃣ Sign Out
**Test**: Click "Thoát" button in user profile

**Expected Results:**
- [ ] Confirmation dialog appears: "Bạn có chắc muốn đăng xuất?"
- [ ] Click OK to confirm
- [ ] User profile disappears
- [ ] Login button reappears
- [ ] Auth hint changes back to blue: "💡 Đăng nhập để lưu..."
- [ ] Favorites section becomes hidden

**Browser Console:**
```
Should see: "👤 User logged out"
```

---

### 8️⃣ Try to Save Without Login
**Test**: Log out, search for place, click "💾 Lưu"

**Expected Results:**
- [ ] Alert appears: "⚠️ Vui lòng đăng nhập để lưu địa điểm yêu thích!"
- [ ] Login popup automatically triggers

---

### 9️⃣ Real-Time Sync Test
**Test**: Open index.html in TWO browser tabs while logged in

**Actions:**
1. In Tab 1: Save a favorite place
2. In Tab 2: Watch the favorites section

**Expected Results:**
- [ ] Tab 2 automatically shows the new favorite (no refresh needed)
- [ ] Both tabs stay in sync

---

### 🔟 Persistence Test
**Test**: Close browser and reopen

**Expected Results:**
- [ ] User is still logged in (persistent session)
- [ ] Favorites are still visible
- [ ] All saved data loads correctly

---

## 🚨 Common Issues & Solutions

### Issue: "Firebase not defined" error
**Solution**: Check internet connection (Firebase SDKs load from CDN)

### Issue: Login popup blocked
**Solution**: Allow popups for localhost in browser settings

### Issue: "Permission denied" when saving
**Solution**: Update Firestore security rules (see FIREBASE_AUTH_GUIDE.md)

### Issue: Favorites not syncing
**Solution**: 
1. Check internet connection
2. Open browser console for errors
3. Verify Firestore is enabled in Firebase Console

### Issue: User profile not showing
**Solution**: Clear browser cache and reload

---

## 🎯 Firebase Console Checks

### In Firebase Console (https://console.firebase.google.com):

1. **Authentication Tab:**
   - [ ] Google Sign-In is enabled
   - [ ] Authorized domains include your domain/localhost
   - [ ] Users list shows logged-in users

2. **Firestore Database Tab:**
   - [ ] Database is created
   - [ ] `favorites` collection exists (after first save)
   - [ ] Documents contain correct fields (uid, name, lat, lon, etc.)
   - [ ] Each favorite has the correct user's UID

3. **Security Rules:**
   - [ ] Rules allow authenticated users to read/write their own data

---

## 📊 Test Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Page Load | ✅ Pass | No errors |
| Google Login | ⏳ Manual Test | Requires user interaction |
| Save Favorite | ⏳ Manual Test | Requires login |
| View on Map | ⏳ Manual Test | Requires saved favorite |
| Remove Favorite | ⏳ Manual Test | Requires saved favorite |
| Sign Out | ⏳ Manual Test | Requires login |
| Real-time Sync | ⏳ Manual Test | Requires multiple tabs |
| Persistence | ⏳ Manual Test | Requires browser restart |

---

## 🎬 Quick Test Script

```
1. Open: http://localhost:8080/index.html
2. Click: "🔐 Đăng nhập Google"
3. Login with Google account
4. Search: "Hà Nội"
5. Click: "💾 Lưu" on first place
6. Check: Favorites section shows saved place
7. Click: "❌" to remove
8. Click: "Thoát" to logout
9. Result: All features working! ✅
```

---

**Testing Started**: December 6, 2025  
**Server**: http://localhost:8080  
**Status**: Ready for manual testing  

👉 **Next Step**: Follow the manual testing steps above to verify all features!
