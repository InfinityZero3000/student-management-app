# Hệ thống Quản lý Sinh viên HUIT

## Giới thiệu
Hệ thống web quản lý sinh viên hiện đại được xây dựng bằng **Flask** với giao diện trực quan và các tính năng mạnh mẽ:

### ✨ Tính năng chính
- 📊 **Dashboard thống kê**: Tổng quan dữ liệu sinh viên với biểu đồ trực quan
- 🔍 **Tìm kiếm nâng cao**: Tìm kiếm chính xác theo MSSV, tên, lớp, ngày sinh
- 📁 **Import đa định dạng**: Hỗ trợ CSV, DOCX, XLSX, TXT
- 📈 **Thống kê chi tiết**: Phân tích điểm số, xếp loại, tỷ lệ đỗ
- 📋 **Quản lý dữ liệu**: Xem, so sánh và xuất báo cáo
- 🎯 **Tìm kiếm thông minh**: Algoritm tìm kiếm với độ chính xác cao

## Yêu cầu hệ thống
- **Python**: 3.8 trở lên
- **RAM**: Tối thiểu 2GB (khuyến nghị 4GB)
- **Dung lượng**: 500MB trống
- **Trình duyệt**: Chrome, Firefox, Safari, Edge (phiên bản mới)

## Cài đặt nhanh

### 1. Clone repository
```bash
git clone https://github.com/InfinityZero3000/student-management-app.git
cd student-management-app
```

### 2. Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# hoặc
.venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies
```bash
cd flask_app
pip install -r requirements.txt
```

### 4. Khởi chạy ứng dụng
```bash
python server.py
```

🌐 Truy cập: **http://127.0.0.1:5002**

## Cấu trúc dự án
```
student-management-app/
├── flask_app/                    # Ứng dụng Flask chính
│   ├── server.py                # Server chính
│   ├── data_processor_new.py    # Xử lý dữ liệu nâng cao
│   ├── file_handler_new.py      # Xử lý file I/O
│   ├── data_comparator.py       # So sánh dữ liệu
│   ├── requirements.txt         # Dependencies
│   ├── static/                  # Tài nguyên tĩnh
│   │   ├── css/style.css       # Stylesheet chính
│   │   └── js/dashboard.js     # JavaScript frontend
│   └── templates/              # Template HTML
│       ├── base.html           # Template cơ sở
│       ├── dashboard.html      # Trang chủ dashboard
│       ├── advanced_search.html # Tìm kiếm nâng cao
│       ├── compare.html        # So sánh dữ liệu
│       ├── data_management.html # Quản lý dữ liệu
│       └── statistics.html     # Thống kê
├── data/                       # Dữ liệu mẫu
│   └── huit_point_student.csv  # File dữ liệu HUIT (3221 records)
└── README.md                   # Tài liệu này
```

