# 📁 Student Management App - File Structure

## 🏗️ **Cấu trúc dự án sau khi tổ chức lại:**

```
student-management-app/
├── flask_app/                    # ← Flask Application
│   ├── server.py                 # ← Flask Backend Server (Python)
│   ├── static/js/
│   │   └── dashboard.js          # ← Frontend JavaScript 
│   ├── templates/                # ← HTML Templates
│   ├── data_comparator.py        # ← Utilities
│   ├── data_processor.py
│   └── file_handler.py
├── data/                         # ← CSV Data Files
├── test_api.py                   # ← API Tests
└── README.md
```

## 🎯 **Phân biệt các file:**

### 🖥️ **Backend (Server)**
- **`server.py`** - Flask web server (Python)
  - Routes, API endpoints
  - Database operations
  - File processing

### 🌐 **Frontend (Client)**  
- **`dashboard.js`** - Browser JavaScript
  - UI interactions
  - Chart rendering
  - AJAX calls

## 🚀 **Cách chạy:**

```bash
cd flask_app
python server.py
```

## 🔧 **Tại sao đổi tên:**

### ❌ **Trước (Gây confusion):**
- `app.py` ← Flask server
- `app.js` ← JavaScript frontend

### ✅ **Sau (Rõ ràng):**
- `server.py` ← Flask backend
- `dashboard.js` ← Frontend JS

## 📋 **Lợi ích:**

1. **Tên file rõ ràng** - Không bị nhầm lẫn
2. **Phân biệt frontend/backend** - Dễ maintain
3. **Tránh conflict** - Không trùng tên
4. **Professional** - Cấu trúc chuẩn
