# Ứng dụng Quản lý Sinh viên

## Mô tả
Ứng dụng web quản lý sinh viên được xây dựng bằng **Streamlit** với các tính năng:
- Import dữ liệu từ CSV/DOCX
- Tính điểm trung bình theo học kỳ
- Tìm kiếm và lọc dữ liệu
- Thống kê và biểu đồ
- Xuất báo cáo Excel/CSV

## Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8+
- pip hoặc conda

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

## Cấu trúc dự án
```
student-management-app/
├── app.py                 # File chính của ứng dụng Streamlit
├── data_processor.py      # Module xử lý dữ liệu
├── file_handler.py        # Module xử lý file I/O
├── requirements.txt       # Dependencies
├── README.md             # Hướng dẫn sử dụng
├── sample_data/          # Dữ liệu mẫu
│   ├── sinh_vien_mau.csv
│   └── diem_so_mau.csv
└── docs/                 # Tài liệu
    └── GUIDE.md
```

## Hướng dẫn sử dụng

### 1. Chuẩn bị dữ liệu

#### File danh sách sinh viên (CSV/DOCX):
Cần có các cột:
- `Ho_Ten`: Họ và tên sinh viên
- `MSSV`: Mã số sinh viên (khóa chính)
- `Lop`: Lớp học

#### File điểm số (CSV):
Cần có các cột:
- `MSSV`: Mã số sinh viên (khóa ngoại)
- `Mon_Hoc`: Tên môn học
- `Diem`: Điểm số (0-10)
- `Hoc_Ky`: Học kỳ (ví dụ: HK1_2023)

### 2. Sử dụng ứng dụng

1. **Upload files**: Chọn file sinh viên và file điểm từ sidebar
2. **Xử lý dữ liệu**: Nhấn nút "Xử lý Dữ liệu"
3. **Khám phá dữ liệu**: Sử dụng các tabs:
   - **Danh sách**: Xem bảng sinh viên
   - **Thống kê**: Xem các chỉ số thống kê
   - **Biểu đồ**: Xem visualization
   - **Xuất dữ liệu**: Tải về CSV/Excel

### 3. Tính năng

#### Tìm kiếm và lọc:
- Tìm kiếm theo tên hoặc MSSV
- Lọc theo lớp
- Lọc theo học kỳ

#### Thống kê:
- Điểm trung bình theo lớp
- Điểm trung bình theo học kỳ
- Phân bố học lực

#### Biểu đồ:
- Bar chart điểm TB theo lớp
- Histogram phân bố điểm
- Box plot điểm theo học kỳ

## Dữ liệu mẫu

Trong ứng dụng có sẵn nút tạo dữ liệu mẫu để demo.

## Lỗi thường gặp

### 1. Lỗi import file
- **Nguyên nhân**: File không đúng định dạng hoặc thiếu cột
- **Giải pháp**: Kiểm tra lại cấu trúc file theo hướng dẫn

### 2. Lỗi encoding
- **Nguyên nhân**: File CSV không đúng encoding
- **Giải pháp**: Lưu file CSV với encoding UTF-8

### 3. Lỗi MSSV không khớp
- **Nguyên nhân**: MSSV trong 2 file không trùng khớp
- **Giải pháp**: Kiểm tra lại MSSV trong cả 2 file

## Mở rộng

Để mở rộng ứng dụng, có thể:
1. Thêm authentication/phân quyền
2. Kết nối database
3. Thêm tính năng báo cáo nâng cao
4. Deploy lên cloud (Streamlit Cloud, Heroku)

## Liên hệ

Nếu có vấn đề, vui lòng tạo issue trên GitHub hoặc liên hệ qua email.
