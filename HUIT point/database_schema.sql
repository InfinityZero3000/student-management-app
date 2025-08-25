-- ==================================================
-- SCRIPT SQL CHO HỆ THỐNG QUẢN LÝ ĐIỂM SINH VIÊN
-- ==================================================

-- 1. TẠO VIEW HỮU ÍCH
-- ==================================================

-- View tổng hợp thông tin sinh viên với điểm
CREATE VIEW IF NOT EXISTS v_student_summary AS
SELECT 
    s.ma_sinh_vien,
    s.ho_dem || ' ' || s.ten AS ho_ten_day_du,
    s.gioi_tinh,
    s.ngay_sinh,
    s.lop,
    s.so_mh_dang_ky,
    s.so_tc_dang_ky,
    s.so_mh_dat,
    
    -- Điểm học kỳ
    sem.diem_10 as diem_hk_10,
    sem.diem_4 as diem_hk_4,
    sem.diem_chu as diem_hk_chu,
    sem.xep_loai_hoc_luc as xep_loai_hk,
    sem.diem_ren_luyen as diem_rl_hk,
    sem.xep_loai_ren_luyen as xep_loai_rl_hk,
    
    -- Điểm tích lũy
    cum.diem_10_tich_luy,
    cum.diem_4_tich_luy,
    cum.diem_chu_tich_luy,
    cum.xep_loai_tich_luy,
    cum.xep_hang,
    cum.nam_thu,
    cum.so_tc_tich_luy,
    cum.diem_ren_luyen_tich_luy,
    cum.xep_loai_ren_luyen_tich_luy,
    cum.ghi_chu,
    
    -- Phân loại
    CASE 
        WHEN cum.diem_4_tich_luy >= 3.60 THEN 'Xuất sắc'
        WHEN cum.diem_4_tich_luy >= 3.20 THEN 'Giỏi'
        WHEN cum.diem_4_tich_luy >= 2.50 THEN 'Khá'
        WHEN cum.diem_4_tich_luy >= 2.00 THEN 'Trung bình'
        WHEN cum.diem_4_tich_luy >= 1.00 THEN 'Yếu'
        ELSE 'Kém'
    END as phan_loai_hoc_luc,
    
    CASE 
        WHEN cum.ghi_chu LIKE '%Cảnh báo%' THEN 'Cảnh báo'
        WHEN cum.ghi_chu LIKE '%Thôi học%' THEN 'Thôi học'
        ELSE 'Bình thường'
    END as tinh_trang_hoc_tap
    
FROM students s
LEFT JOIN semester_scores sem ON s.ma_sinh_vien = sem.ma_sinh_vien
LEFT JOIN cumulative_scores cum ON s.ma_sinh_vien = cum.ma_sinh_vien;

-- View sinh viên lớp 14 điểm cao
CREATE VIEW IF NOT EXISTS v_students_class14_high_gpa AS
SELECT * 
FROM v_student_summary 
WHERE lop LIKE '%14%' 
  AND diem_4_tich_luy >= 3.4
ORDER BY diem_4_tich_luy DESC;

-- View thống kê theo lớp
CREATE VIEW IF NOT EXISTS v_class_statistics AS
SELECT 
    lop,
    COUNT(*) as so_luong_sv,
    COUNT(CASE WHEN diem_4_tich_luy >= 3.6 THEN 1 END) as sv_xuat_sac,
    COUNT(CASE WHEN diem_4_tich_luy >= 3.2 AND diem_4_tich_luy < 3.6 THEN 1 END) as sv_gioi,
    COUNT(CASE WHEN diem_4_tich_luy >= 2.5 AND diem_4_tich_luy < 3.2 THEN 1 END) as sv_kha,
    COUNT(CASE WHEN diem_4_tich_luy >= 2.0 AND diem_4_tich_luy < 2.5 THEN 1 END) as sv_trung_binh,
    COUNT(CASE WHEN diem_4_tich_luy < 2.0 THEN 1 END) as sv_yeu_kem,
    AVG(diem_4_tich_luy) as diem_tb_lop,
    MAX(diem_4_tich_luy) as diem_cao_nhat,
    MIN(diem_4_tich_luy) as diem_thap_nhat
FROM v_student_summary
WHERE diem_4_tich_luy IS NOT NULL
GROUP BY lop
ORDER BY diem_tb_lop DESC;

-- ==================================================
-- 2. CÁC TRUY VẤN HỮU ÍCH
-- ==================================================

-- Query 1: Top 10 sinh viên điểm cao nhất toàn trường
/*
SELECT 
    ma_sinh_vien,
    ho_ten_day_du,
    lop,
    diem_4_tich_luy,
    xep_loai_tich_luy,
    so_tc_tich_luy
FROM v_student_summary 
WHERE diem_4_tich_luy IS NOT NULL
ORDER BY diem_4_tich_luy DESC 
LIMIT 10;
*/

-- Query 2: Danh sách sinh viên cảnh báo học vụ
/*
SELECT 
    ma_sinh_vien,
    ho_ten_day_du,
    lop,
    diem_4_tich_luy,
    ghi_chu
FROM v_student_summary 
WHERE tinh_trang_hoc_tap = 'Cảnh báo'
ORDER BY lop, ho_ten_day_du;
*/

-- Query 3: Thống kê sinh viên theo khóa
/*
SELECT 
    SUBSTR(lop, 1, 2) as khoa,
    COUNT(*) as tong_sv,
    COUNT(CASE WHEN diem_4_tich_luy >= 3.4 THEN 1 END) as sv_gioi_xuat_sac,
    ROUND(AVG(diem_4_tich_luy), 2) as diem_tb_khoa
FROM v_student_summary
WHERE diem_4_tich_luy IS NOT NULL
GROUP BY SUBSTR(lop, 1, 2)
ORDER BY khoa;
*/

-- Query 4: Tìm sinh viên có số tín chỉ tích lũy thấp
/*
SELECT 
    ma_sinh_vien,
    ho_ten_day_du,
    lop,
    so_tc_tich_luy,
    nam_thu,
    diem_4_tich_luy,
    ghi_chu
FROM v_student_summary 
WHERE so_tc_tich_luy < 50 AND nam_thu >= 3
ORDER BY so_tc_tich_luy ASC;
*/

-- Query 5: Phân bố điểm theo từng lớp 14
/*
SELECT 
    lop,
    so_luong_sv,
    sv_xuat_sac,
    sv_gioi,
    sv_kha,
    sv_trung_binh,
    sv_yeu_kem,
    ROUND(diem_tb_lop, 2) as diem_tb_lop,
    ROUND(diem_cao_nhat, 2) as diem_cao_nhat
FROM v_class_statistics 
WHERE lop LIKE '%14%'
ORDER BY diem_tb_lop DESC;
*/

-- ==================================================
-- 3. CÁC INDEX ĐỂ TỐI ƯU HIỆU SUẤT
-- ==================================================

CREATE INDEX IF NOT EXISTS idx_students_lop ON students(lop);
CREATE INDEX IF NOT EXISTS idx_students_ma_sv ON students(ma_sinh_vien);
CREATE INDEX IF NOT EXISTS idx_cumulative_diem_4 ON cumulative_scores(diem_4_tich_luy);
CREATE INDEX IF NOT EXISTS idx_cumulative_ma_sv ON cumulative_scores(ma_sinh_vien);
CREATE INDEX IF NOT EXISTS idx_semester_ma_sv ON semester_scores(ma_sinh_vien);

-- ==================================================
-- 4. TRIGGER ĐỂ TỰ ĐỘNG CẬP NHẬT THỐNG KÊ
-- ==================================================

-- Tạo bảng log để theo dõi thay đổi
CREATE TABLE IF NOT EXISTS student_changes_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ma_sinh_vien TEXT,
    change_type TEXT, -- INSERT, UPDATE, DELETE
    old_gpa REAL,
    new_gpa REAL,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger khi cập nhật điểm
CREATE TRIGGER IF NOT EXISTS tr_update_gpa_log
AFTER UPDATE OF diem_4_tich_luy ON cumulative_scores
BEGIN
    INSERT INTO student_changes_log (
        ma_sinh_vien, 
        change_type, 
        old_gpa, 
        new_gpa
    ) VALUES (
        NEW.ma_sinh_vien,
        'UPDATE',
        OLD.diem_4_tich_luy,
        NEW.diem_4_tich_luy
    );
END;

-- ==================================================
-- 5. STORED PROCEDURES (SQLite không hỗ trợ, dùng Python thay thế)
-- ==================================================

/*
Các function Python có thể thêm vào class StudentDatabaseProcessor:

def get_top_students(self, limit=10):
    "Lấy top sinh viên điểm cao nhất"
    
def get_students_at_risk(self):
    "Lấy danh sách sinh viên cảnh báo"
    
def get_class_statistics(self, class_pattern='%14%'):
    "Thống kê theo lớp"
    
def search_students(self, keyword):
    "Tìm kiếm sinh viên theo từ khóa"
    
def export_transcript(self, student_id):
    "Xuất bảng điểm sinh viên"
*/
