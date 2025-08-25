#!/usr/bin/env python3
"""
Script xử lý database cho file điểm sinh viên
Yêu cầu:
1. Tạo cấu trúc lưu dữ liệu SQL
2. Truy vấn lọc sinh viên lớp 14, điểm TB >= 3.4
"""

import sqlite3
import pandas as pd
import os
import re
from datetime import datetime

class StudentDatabaseProcessor:
    def __init__(self, db_name="student_scores.db"):
        """Khởi tạo database processor"""
        self.db_name = db_name
        self.conn = None
        
    def connect_database(self):
        """Kết nối tới database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"[check-circle] Đã kết nối database: {self.db_name}")
            return True
        except Exception as e:
            print(f"[x-circle] Lỗi kết nối database: {e}")
            return False
    
    def create_tables(self):
        """Tạo cấu trúc bảng SQL"""
        
        if not self.conn:
            print("[x-circle] Chưa kết nối database!")
            return False
            
        try:
            cursor = self.conn.cursor()
            
            # Tạo bảng sinh viên chính
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stt INTEGER,
                    ma_sinh_vien TEXT UNIQUE NOT NULL,
                    ho_dem TEXT,
                    ten TEXT,
                    gioi_tinh TEXT,
                    ngay_sinh DATE,
                    lop TEXT,
                    so_mh_dang_ky INTEGER,
                    so_tc_dang_ky INTEGER,
                    so_mh_dat INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tạo bảng điểm học kỳ
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS semester_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ma_sinh_vien TEXT,
                    diem_10 REAL,
                    diem_4 REAL,
                    diem_chu TEXT,
                    xep_loai_hoc_luc TEXT,
                    diem_ren_luyen INTEGER,
                    xep_loai_ren_luyen TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ma_sinh_vien) REFERENCES students (ma_sinh_vien)
                )
            ''')
            
            # Tạo bảng điểm tích lũy
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cumulative_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ma_sinh_vien TEXT,
                    diem_10_tich_luy REAL,
                    diem_4_tich_luy REAL,
                    diem_chu_tich_luy TEXT,
                    xep_loai_tich_luy TEXT,
                    xep_hang TEXT,
                    nam_thu INTEGER,
                    so_tc_tich_luy INTEGER,
                    diem_ren_luyen_tich_luy INTEGER,
                    xep_loai_ren_luyen_tich_luy TEXT,
                    ghi_chu TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ma_sinh_vien) REFERENCES students (ma_sinh_vien)
                )
            ''')
            
            self.conn.commit()
            print("[check-circle] Đã tạo thành công cấu trúc database!")
            print("[clipboard] Các bảng đã tạo:")
            print("   • students: Thông tin sinh viên")
            print("   • semester_scores: Điểm học kỳ")
            print("   • cumulative_scores: Điểm tích lũy")
            
            return True
            
        except Exception as e:
            print(f"[x-circle] Lỗi tạo bảng: {e}")
            return False
    
    def parse_csv_data(self, csv_file_path):
        """Phân tích và làm sạch dữ liệu CSV"""
        
        print(f"📖 Đang đọc file: {csv_file_path}")
        
        try:
            # Đọc file CSV với dtype để giữ mã sinh viên dạng string
            df = pd.read_csv(csv_file_path, encoding='utf-8', dtype={'Mã sinh viên': str})
            
            print(f"[clipboard] Columns trong file: {len(df.columns)} cột")
            print(f"[bar-chart] Shape: {df.shape}")
            
            # Loại bỏ các dòng trống
            df = df.dropna(subset=['Mã sinh viên'])
            
            # Convert mã sinh viên về dạng string và làm sạch
            df['Mã sinh viên'] = df['Mã sinh viên'].astype(str)
            
            # Làm sạch dữ liệu - chỉ giữ các dòng có mã sinh viên hợp lệ (10 chữ số)
            df = df[df['Mã sinh viên'].str.match(r'^\d{10}$')]
            
            print(f"[check-circle] Đã đọc {len(df)} records hợp lệ")
            
            # In một vài mẫu để kiểm tra
            if len(df) > 0:
                print("[clipboard] Mẫu dữ liệu:")
                for i in range(min(3, len(df))):
                    row = df.iloc[i]
                    print(f"  {row['Mã sinh viên']} - {row['Họ đệm']} {row['Tên']} - Lớp: {row['Lớp']}")
            
            return df
            
        except Exception as e:
            print(f"[x-circle] Lỗi đọc CSV: {e}")
            return None
    
    def clean_numeric_data(self, value):
        """Làm sạch dữ liệu số"""
        if pd.isna(value) or value == '' or value == ' ':
            return None
        try:
            return float(str(value).strip())
        except:
            return None
    
    def clean_text_data(self, value):
        """Làm sạch dữ liệu text"""
        if pd.isna(value):
            return None
        return str(value).strip()
    
    def insert_data(self, df):
        """Chèn dữ liệu vào database"""
        
        if not self.conn or df is None:
            print("[x-circle] Không thể insert dữ liệu!")
            return False
        
        try:
            cursor = self.conn.cursor()
            inserted_count = 0
            
            print("[save] Bắt đầu insert dữ liệu...")
            print(f"[clipboard] Columns available: {list(df.columns)}")
            
            # Map columns dựa trên index vì có unnamed columns
            expected_cols = ['STT', 'Mã sinh viên', 'Họ đệm', 'Tên', 'Giới tính', 'Ngày sinh', 'Lớp', 
                           'Số MH đăng ký', 'Số TC đăng ký', 'Số MH đạt']
            
            # Điểm học kỳ ở columns 10-15
            semester_score_cols = [10, 11, 12, 13, 14, 15]  # Điểm 10, Điểm 4, Điểm chữ, Xếp loại, Điểm rèn luyện, Xếp loại rèn luyện
            
            # Điểm tích lũy ở columns 16-25  
            cumulative_score_cols = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25]  # Điểm 10, Điểm 4, Điểm chữ, Xếp loại, Xếp hạng, Năm thứ, Số TC, Điểm rèn luyện, Xếp loại rèn luyện, Ghi chú
            
            for index, row in df.iterrows():
                try:
                    ma_sv = self.clean_text_data(row['Mã sinh viên'])
                    if not ma_sv:
                        continue
                    
                    # Insert vào bảng students
                    cursor.execute('''
                        INSERT OR REPLACE INTO students 
                        (stt, ma_sinh_vien, ho_dem, ten, gioi_tinh, ngay_sinh, lop, 
                         so_mh_dang_ky, so_tc_dang_ky, so_mh_dat)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        self.clean_numeric_data(row['STT']),
                        ma_sv,
                        self.clean_text_data(row['Họ đệm']),
                        self.clean_text_data(row['Tên']),
                        self.clean_text_data(row['Giới tính']),
                        self.clean_text_data(row['Ngày sinh']),
                        self.clean_text_data(row['Lớp']),
                        self.clean_numeric_data(row['Số MH đăng ký']),
                        self.clean_numeric_data(row['Số TC đăng ký']),
                        self.clean_numeric_data(row['Số MH đạt'])
                    ))
                    
                    # Insert vào bảng semester_scores - dùng index vì có unnamed columns
                    cursor.execute('''
                        INSERT OR REPLACE INTO semester_scores 
                        (ma_sinh_vien, diem_10, diem_4, diem_chu, xep_loai_hoc_luc, 
                         diem_ren_luyen, xep_loai_ren_luyen)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        ma_sv,
                        self.clean_numeric_data(row.iloc[10]),  # Điểm 10
                        self.clean_numeric_data(row.iloc[11]),  # Điểm 4
                        self.clean_text_data(row.iloc[12]),     # Điểm chữ
                        self.clean_text_data(row.iloc[13]),     # Xếp loại
                        self.clean_numeric_data(row.iloc[14]),  # Điểm rèn luyện
                        self.clean_text_data(row.iloc[15])      # Xếp loại rèn luyện
                    ))
                    
                    # Insert vào bảng cumulative_scores
                    cursor.execute('''
                        INSERT OR REPLACE INTO cumulative_scores 
                        (ma_sinh_vien, diem_10_tich_luy, diem_4_tich_luy, diem_chu_tich_luy, 
                         xep_loai_tich_luy, xep_hang, nam_thu, so_tc_tich_luy, 
                         diem_ren_luyen_tich_luy, xep_loai_ren_luyen_tich_luy, ghi_chu)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        ma_sv,
                        self.clean_numeric_data(row.iloc[16]),  # Điểm 10 tích lũy
                        self.clean_numeric_data(row.iloc[17]),  # Điểm 4 tích lũy
                        self.clean_text_data(row.iloc[18]),     # Điểm chữ tích lũy
                        self.clean_text_data(row.iloc[19]),     # Xếp loại tích lũy
                        self.clean_text_data(row.iloc[20]),     # Xếp hạng
                        self.clean_numeric_data(row.iloc[21]),  # Năm thứ
                        self.clean_numeric_data(row.iloc[22]),  # Số TC tích lũy
                        self.clean_numeric_data(row.iloc[23]),  # Điểm rèn luyện tích lũy
                        self.clean_text_data(row.iloc[24]),     # Xếp loại rèn luyện tích lũy
                        self.clean_text_data(row.iloc[25])      # Ghi chú
                    ))
                    
                    inserted_count += 1
                    
                    if inserted_count % 100 == 0:
                        print(f"Đã insert: {inserted_count} records...")
                        
                except Exception as e:
                    print(f"[alert-triangle] Lỗi insert record {ma_sv}: {e}")
                    continue
            
            self.conn.commit()
            print(f"[check-circle] Đã insert thành công {inserted_count} records!")
            return True
            
        except Exception as e:
            print(f"[x-circle] Lỗi insert dữ liệu: {e}")
            return False
    
    def query_class_14_gpa_above_34(self):
        """Truy vấn sinh viên lớp 14, điểm TB >= 3.4"""
        
        if not self.conn:
            print("[x-circle] Chưa kết nối database!")
            return None
        
        try:
            print("[search] TRUY VẤN SINH VIÊN LỚP CHỨA '14', ĐIỂM TB >= 3.4")
            print("=" * 60)
            
            # Trước tiên, kiểm tra các lớp có sẵn
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT lop FROM students ORDER BY lop")
            all_classes = cursor.fetchall()
            
            print("📚 Các lớp có trong database:")
            class_14_list = []
            for (lop,) in all_classes:
                if lop and '14' in str(lop):
                    class_14_list.append(lop)
                    print(f"  ✓ {lop}")
                else:
                    print(f"    {lop}")
            
            if not class_14_list:
                print("[x-circle] Không tìm thấy lớp nào chứa '14'!")
                return []
            
            print(f"\n🎯 Tìm thấy {len(class_14_list)} lớp chứa '14'")
            
            query = '''
                SELECT DISTINCT
                    s.ma_sinh_vien,
                    s.ho_dem,
                    s.ten,
                    s.lop,
                    cs.diem_4_tich_luy as diem_trung_binh,
                    cs.xep_loai_tich_luy,
                    cs.so_tc_tich_luy,
                    cs.ghi_chu
                FROM students s
                JOIN cumulative_scores cs ON s.ma_sinh_vien = cs.ma_sinh_vien
                WHERE (s.lop LIKE '%14%' OR s.lop LIKE '%14DHBM%' OR s.lop LIKE '%DHBM14%')
                    AND cs.diem_4_tich_luy >= 3.4
                    AND cs.diem_4_tich_luy IS NOT NULL
                ORDER BY cs.diem_4_tich_luy DESC, s.ma_sinh_vien
            '''
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                print(f"[check-circle] Tìm thấy {len(results)} sinh viên thỏa mãn điều kiện:")
                print()
                
                # In header
                print(f"{'STT':<4} {'Mã SV':<12} {'Họ Tên':<30} {'Lớp':<15} {'ĐTB':<6} {'Xếp Loại':<15} {'TC':<4} {'Ghi Chú':<20}")
                print("-" * 110)
                
                # In từng record
                for i, row in enumerate(results, 1):
                    ma_sv, ho_dem, ten, lop, dtb, xep_loai, tc, ghi_chu = row
                    ho_ten = f"{ho_dem or ''} {ten or ''}".strip()
                    
                    print(f"{i:<4} {ma_sv:<12} {ho_ten:<30} {lop:<15} {dtb:<6.2f} {xep_loai or '':<15} {tc or 0:<4} {ghi_chu or '':<20}")
                
                # Thống kê
                print(f"\n📊 THỐNG KÊ:")
                print(f"• Tổng số sinh viên thỏa mãn: {len(results)}")
                
                # Phân bố theo lớp
                class_stats = {}
                for row in results:
                    lop = row[3]
                    class_stats[lop] = class_stats.get(lop, 0) + 1
                
                print("• Phân bố theo lớp:")
                for lop, count in sorted(class_stats.items()):
                    print(f"  - {lop}: {count} sinh viên")
                
                # Điểm trung bình cao nhất, thấp nhất
                scores = [row[4] for row in results if row[4] is not None]
                if scores:
                    print(f"• Điểm TB cao nhất: {max(scores):.2f}")
                    print(f"• Điểm TB thấp nhất: {min(scores):.2f}")
                    print(f"• Điểm TB trung bình: {sum(scores)/len(scores):.2f}")
                
                return results
                
            else:
                print("[x-circle] Không tìm thấy sinh viên nào thỏa mãn điều kiện!")
                return []
                
        except Exception as e:
            print(f"[x-circle] Lỗi truy vấn: {e}")
            return None
    
    def export_query_results(self, results, output_file="query_results.csv"):
        """Export kết quả query ra CSV"""
        
        if not results:
            print("[x-circle] Không có dữ liệu để export!")
            return False
        
        try:
            # Tạo DataFrame
            df = pd.DataFrame(results, columns=[
                'Mã Sinh Viên', 'Họ Đệm', 'Tên', 'Lớp', 
                'Điểm TB', 'Xếp Loại', 'TC Tích Lũy', 'Ghi Chú'
            ])
            
            # Tạo cột họ tên đầy đủ
            df['Họ Tên'] = (df['Họ Đệm'].fillna('') + ' ' + df['Tên'].fillna('')).str.strip()
            
            # Sắp xếp lại cột
            df = df[['Mã Sinh Viên', 'Họ Tên', 'Lớp', 'Điểm TB', 'Xếp Loại', 'TC Tích Lũy', 'Ghi Chú']]
            
            # Export
            df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"[check-circle] Đã export kết quả ra: {output_file}")
            
            return True
            
        except Exception as e:
            print(f"[x-circle] Lỗi export: {e}")
            return False
    
    def show_database_stats(self):
        """Hiển thị thống kê database"""
        
        if not self.conn:
            print("[x-circle] Chưa kết nối database!")
            return
        
        try:
            cursor = self.conn.cursor()
            
            print("\n📊 THỐNG KÊ DATABASE:")
            print("=" * 40)
            
            # Đếm sinh viên
            cursor.execute("SELECT COUNT(*) FROM students")
            student_count = cursor.fetchone()[0]
            print(f"• Tổng số sinh viên: {student_count:,}")
            
            # Đếm theo lớp chứa 14
            cursor.execute("""
                SELECT lop, COUNT(*) 
                FROM students 
                WHERE lop LIKE '%14%' OR lop LIKE '%14DHBM%' OR lop LIKE '%DHBM14%'
                GROUP BY lop 
                ORDER BY lop
            """)
            class_14_stats = cursor.fetchall()
            
            print(f"• Sinh viên lớp chứa '14':")
            total_class_14 = 0
            for lop, count in class_14_stats:
                print(f"  - {lop}: {count} sinh viên")
                total_class_14 += count
            print(f"  TỔNG: {total_class_14} sinh viên")
            
            # Đếm sinh viên có điểm >= 3.4
            cursor.execute("""
                SELECT COUNT(*) 
                FROM cumulative_scores 
                WHERE diem_4_tich_luy >= 3.4
            """)
            good_students = cursor.fetchone()[0]
            print(f"• Sinh viên có ĐTB >= 3.4: {good_students}")
            
            # Hiển thị một vài lớp mẫu
            cursor.execute("SELECT DISTINCT lop FROM students LIMIT 10")
            sample_classes = cursor.fetchall()
            print(f"• Mẫu các lớp trong DB:")
            for (lop,) in sample_classes:
                print(f"  - {lop}")
            
        except Exception as e:
            print(f"[x-circle] Lỗi thống kê: {e}")
    
    def close_connection(self):
        """Đóng kết nối database"""
        if self.conn:
            self.conn.close()
            print("[check-circle] Đã đóng kết nối database")

def main():
    """Hàm chính"""
    
    print("[database] SCRIPT XỬ LÝ DATABASE ĐIỂM SINH VIÊN")
    print("=" * 50)
    
    # Khởi tạo processor
    processor = StudentDatabaseProcessor()
    
    # Kết nối database
    if not processor.connect_database():
        return
    
    # Tạo cấu trúc bảng
    if not processor.create_tables():
        processor.close_connection()
        return
    
    # Đường dẫn file CSV
    csv_file = "/Users/nguyenhuuthang/Documents/Data/huit_data_point.csv"
    
    if not os.path.exists(csv_file):
        print(f"[x-circle] Không tìm thấy file: {csv_file}")
        processor.close_connection()
        return
    
    # Đọc và insert dữ liệu
    df = processor.parse_csv_data(csv_file)
    if df is not None:
        if processor.insert_data(df):
            print("[check-circle] Hoàn thành việc import dữ liệu!")
        else:
            print("[x-circle] Lỗi import dữ liệu!")
            processor.close_connection()
            return
    else:
        processor.close_connection()
        return
    
    # Hiển thị thống kê
    processor.show_database_stats()
    
    # Thực hiện truy vấn chính
    print("\n" + "="*60)
    results = processor.query_class_14_gpa_above_34()
    
    # Export kết quả
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"sinh_vien_lop14_dtb_tren_3.4_{timestamp}.csv"
        processor.export_query_results(results, output_file)
    
    # Đóng kết nối
    processor.close_connection()
    
    print("\n🎉 HOÀN THÀNH!")

if __name__ == "__main__":
    main()
