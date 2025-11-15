# Tìm Điểm Du Lịch Việt Nam 🗺️

Ứng dụng web cho phép người dùng tìm kiếm địa điểm ở Việt Nam và hiển thị 5 điểm thú vị (Points of Interest) gần đó trên bản đồ.

## Tính Năng

✨ **Các tính năng chính:**
- 🔍 Tìm kiếm địa điểm ở Việt Nam (thành phố, quận, phố, địa danh...)
- 🗺️ Hiển thị vị trí trên bản đồ tương tác (Leaflet + OpenStreetMap)
- 📍 Tự động tìm và hiển thị 5 điểm thú vị gần đó:
  - Điểm du lịch (tourism)
  - Nhà hàng, quán café (amenity)
  - Di tích lịch sử (historic)
- 💡 Giao diện đẹp, responsive với Tailwind CSS
- 🎯 Click vào điểm thú vị để xem chi tiết trên bản đồ

## Công Nghệ Sử Dụng

- **Leaflet.js** - Thư viện bản đồ tương tác
- **OpenStreetMap** - Dữ liệu bản đồ
- **Nominatim API** - Geocoding (chuyển tên địa điểm thành tọa độ)
- **Overpass API** - Tìm kiếm Points of Interest từ OpenStreetMap
- **Tailwind CSS** - Styling framework

## Cách Chạy

### Phương pháp 1: Sử dụng Python HTTP Server

```bash
# Mở terminal trong thư mục dự án
cd /workspaces/CT_Week5_24125093

# Chạy server (Python 3)
python3 -m http.server 8000

# Mở trình duyệt và truy cập:
# http://localhost:8000/index.html
```

### Phương pháp 2: Sử dụng npx serve

```bash
# Chạy từ thư mục dự án
npx serve . -l 5000

# Mở trình duyệt và truy cập:
# http://localhost:5000/index.html
```

### Phương pháp 3: Mở trực tiếp file

Bạn cũng có thể mở file `index.html` trực tiếp trong trình duyệt (double-click), nhưng nên dùng HTTP server để tránh lỗi CORS.

## Hướng Dẫn Sử Dụng

1. **Nhập tên địa điểm** vào ô tìm kiếm (ví dụ: "Hà Nội", "Đà Nẵng", "Hội An", "Phố cổ Hà Nội")
2. **Nhấn nút "🔍 Tìm kiếm"** hoặc Enter
3. **Chờ ứng dụng** tìm kiếm và hiển thị:
   - Vị trí chính trên bản đồ (marker đỏ 📍)
   - 5 điểm thú vị gần đó (marker xanh với số thứ tự)
   - Danh sách điểm thú vị bên dưới
4. **Click vào card** của điểm thú vị để xem chi tiết trên bản đồ

## Ví Dụ Tìm Kiếm

Bạn có thể thử các địa điểm sau:
- Hà Nội
- Hội An
- Đà Nẵng
- Nha Trang
- Sài Gòn / TP Hồ Chí Minh
- Phố cổ Hà Nội
- Bãi biển Mỹ Khê
- Chùa Một Cột

## Cấu Trúc Dự Án

```
CT_Week5_24125093/
├── index.html          # Ứng dụng chính (HTML + CSS + JavaScript)
├── main.html           # Firebase demo cũ
└── README.md           # Tài liệu này
```

## API Sử Dụng

### 1. Nominatim API (Geocoding)
- URL: `https://nominatim.openstreetmap.org/search`
- Chức năng: Chuyển tên địa điểm → tọa độ (lat, lon)
- Miễn phí, không cần API key

### 2. Overpass API (POI Search)
- URL: `https://overpass-api.de/api/interpreter`
- Chức năng: Tìm điểm thú vị trong bán kính 5km
- Miễn phí, không cần API key

## Lưu Ý

- ✅ Ứng dụng hoàn toàn miễn phí, không cần đăng ký API key
- ✅ Hoạt động offline sau khi tải xong (trừ việc gọi API)
- ⚠️ Nominatim có rate limit: 1 request/giây - đủ cho sử dụng bình thường
- ⚠️ Kết quả phụ thuộc vào dữ liệu OpenStreetMap (có thể không đầy đủ ở một số vùng)

## Xử Lý Lỗi

Nếu không tìm thấy kết quả:
1. Thử tên địa điểm cụ thể hơn (ví dụ: "Hà Nội" thay vì "HN")
2. Thử địa điểm lớn hơn (thành phố thay vì phố nhỏ)
3. Kiểm tra kết nối internet
4. Một số vùng có thể có ít dữ liệu POI trên OpenStreetMap

## Tác Giả

Dự án CT Week 5 - 24125093

## License

MIT License - Tự do sử dụng cho mục đích học tập và cá nhân.