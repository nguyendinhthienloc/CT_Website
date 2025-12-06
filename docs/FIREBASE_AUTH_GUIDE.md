# 🔐 Firebase Authentication & Favorites Guide

## ✨ Features Added

### 1. **Google Sign-In Authentication**
- Users can log in with their Google account
- Persistent login across sessions
- Beautiful user profile display with avatar

### 2. **Save Favorite Places**
- Logged-in users can save their favorite places
- Each favorite is stored in Firebase Firestore
- Favorites are synced in real-time across devices

### 3. **User-Specific Data**
- Each user has their own favorites collection
- Data is private and secure (filtered by user ID)
- Automatic real-time updates when favorites change

## 🎯 How to Use

### For Users:

1. **Login**
   - Click the "🔐 Đăng nhập Google" button in the header
   - Authorize with your Google account
   - Your profile will appear in the top-right corner

2. **Save Favorites**
   - Search for a location (e.g., "Hà Nội", "Đà Nẵng")
   - Browse the 5 interesting places shown
   - Click the "💾 Lưu" button on any place you like
   - A success notification will appear

3. **View Favorites**
   - Your saved favorites appear in the "⭐ Địa điểm yêu thích của bạn" section
   - Click "🗺️ Xem trên bản đồ" to navigate to that location
   - Click "❌" to remove a favorite

4. **Logout**
   - Click the "Thoát" button in your profile chip

## 🔧 Technical Details

### Firebase Configuration
- **Project**: ct-week5-24125093
- **Auth Provider**: Google Sign-In
- **Database**: Cloud Firestore

### Firestore Collections

#### `favorites` Collection
Each document contains:
```javascript
{
  uid: "user-id",           // Firebase Auth user ID
  name: "Place Name",       // Name of the place
  type: "Category",         // Type/category (e.g., "Restaurant", "Museum")
  lat: 16.0544,            // Latitude
  lon: 108.2022,           // Longitude
  icon: "🏛️",              // Emoji icon
  address: "Address",      // Optional address
  createdAt: Timestamp     // When it was saved
}
```

### Security Rules (Recommended for Firestore)

Add these rules to your Firebase Console → Firestore Database → Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own favorites
    match /favorites/{favoriteId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.uid;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.uid;
    }
  }
}
```

## 🚀 Implementation Files

### Modified Files:
- **index.html** - Main application with Firebase integration

### Existing Firebase Implementation:
- **main.html** - Example Firebase app with notes feature (reference)

## 🎨 UI Components Added

1. **Auth Header Section**
   - Login button (hidden when logged in)
   - User profile chip with avatar (visible when logged in)
   - Logout button
   - Status hint message

2. **Favorites Section**
   - Grid of saved favorite places
   - Each card shows: icon, name, type, address, save date
   - Actions: View on map, Remove from favorites
   - Empty state when no favorites

3. **POI Card Updates**
   - "💾 Lưu" button on each place card
   - Gradient amber/orange styling for save button
   - Success notification on save

## 🔍 Code Structure

### Authentication Flow:
```javascript
1. User clicks login → signInWithPopup()
2. onAuthStateChanged() detects login
3. UI updates to show user profile
4. Firestore query subscribes to user's favorites
5. Real-time updates display saved places
```

### Save Favorite Flow:
```javascript
1. User clicks "💾 Lưu" on a POI card
2. Check if user is logged in
3. Add document to Firestore 'favorites' collection
4. Real-time listener updates the favorites section
5. Success notification appears
```

## 📱 Responsive Design

- Mobile-friendly layout
- Flexbox and Grid for responsive cards
- Touch-friendly buttons
- Smooth scrolling and animations

## 🐛 Troubleshooting

### Login doesn't work:
- Check if Firebase project has Google Sign-In enabled
- Verify the authorized domains in Firebase Console
- Check browser console for errors

### Favorites not saving:
- Ensure user is logged in
- Check Firestore rules allow writes
- Verify Firebase config is correct
- Check browser console for errors

### Data not syncing:
- Check internet connection
- Verify Firestore real-time listeners are active
- Check browser console for quota/permission errors

## 🎉 Next Steps

You can extend this with:
- Email/password authentication
- Social sharing of favorite places
- Comments and ratings
- Export favorites to JSON/CSV
- Search within favorites
- Categories and tags for favorites

---

**Created**: December 2025  
**Firebase SDK**: v10.12.5  
**Framework**: Vanilla JavaScript + Tailwind CSS
