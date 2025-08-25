"""
Module xử lý và phân tích dữ liệu sinh viên HUIT
Chức năng: Phân tích dữ liệu sinh viên, thống kê, báo cáo
Hỗ trợ đọc định dạng dữ liệu đặc thù từ hệ thống của HUIT
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import re

class DataProcessor:
    """Class xử lý dữ liệu sinh viên và điểm số"""
    
    def __init__(self):
        # Cấu trúc cột dữ liệu sinh viên HUIT
        self.columns_mapping = {
            'mssv': ['Mã sinh viên', 'Mã Sinh Viên', 'MSSV', 'Ma_Sinh_Vien'],
            'ho': ['Họ đệm', 'Ho_Dem', 'Ho'],
            'ten': ['Tên', 'Ten'],
            'ho_ten': ['Họ và tên', 'Họ Tên', 'Ho_Ten'],
            'gioi_tinh': ['Giới tính', 'Gioi_Tinh', 'Gender'],
            'ngay_sinh': ['Ngày sinh', 'Ngay_Sinh', 'DOB'],
            'lop': ['Lớp', 'Lop', 'Class'],
            'so_mh_dang_ky': ['Số MH đăng ký', 'So_MH_Dang_Ky'],
            'so_tc_dang_ky': ['Số TC đăng ký', 'So_TC_Dang_Ky'],
            'so_mh_dat': ['Số MH đạt', 'So_MH_Dat'],
            'diem_10': ['Điểm 10', 'Diem_10'],
            'diem_4': ['Điểm 4', 'Diem_4'],
            'diem_chu': ['Điểm chữ', 'Diem_Chu'],
            'xep_loai': ['Xếp loại', 'Xep_Loai', 'Rank'],
            'diem_ren_luyen': ['Điểm', 'Diem_Ren_Luyen'],
            'xep_loai_rl': ['Xếp loại', 'Xep_Loai_Ren_Luyen'],
            'nam_thu': ['Năm thứ', 'Nam_Thu', 'Year'],
            'so_tc_tich_luy': ['Số TC tích lũy', 'So_TC_Tich_Luy', 'Credits'],
            'ghi_chu': ['Ghi chú', 'Ghi_Chu', 'Note'],
        }
        
        # Cấu hình trích xuất dữ liệu từ file HUIT Point
        self.column_groups = {
            'thong_tin_ca_nhan': ['STT', 'Mã sinh viên', 'Họ đệm', 'Tên', 'Giới tính', 'Ngày sinh', 'Lớp'],
            'dang_ky_hoc': ['Số MH đăng ký', 'Số TC đăng ký', 'Số MH đạt'],
            'diem_hoc_ky': ['Điểm 10', 'Điểm 4', 'Điểm chữ', 'Xếp loại'],
            'diem_ren_luyen': ['Điểm', 'Xếp loại'],
            'tich_luy': ['Điểm 10', 'Điểm 4', 'Điểm chữ', 'Xếp loại', 'Xếp hạng', 'Năm thứ', 'Số TC tích lũy', 'Điểm', 'Xếp loại', 'Ghi chú']
        }
    
    def load_and_process_data(self, file_path: str) -> pd.DataFrame:
        """
        Đọc và xử lý dữ liệu sinh viên từ CSV
        
        Args:
            file_path: Đường dẫn đến file CSV
            
        Returns:
            DataFrame đã được xử lý
        """
        try:
            # Đọc file CSV với encoding phù hợp
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # Kiểm tra nếu là định dạng của HUIT
            if self._is_huit_format(df):
                return self._process_huit_data(df)
                
            # Chuẩn hóa tên cột
            df = self._normalize_column_names(df)
            
            # Xử lý dữ liệu
            df = self._clean_data(df)
            
            # Thêm các cột phân tích
            df = self._add_analysis_columns(df)
            
            return df
            
        except Exception as e:
            print(f"Lỗi xử lý dữ liệu: {str(e)}")
            return pd.DataFrame()
    
    def _is_huit_format(self, df: pd.DataFrame) -> bool:
        """
        Kiểm tra xem dữ liệu có phải định dạng đặc thù của HUIT không
        """
        required_columns = ['Mã sinh viên', 'Họ đệm', 'Tên', 'Lớp', 'Số TC tích lũy']
        for col in required_columns:
            if col not in df.columns:
                return False
        return True
    
    def _process_huit_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Xử lý dữ liệu đặc thù từ HUIT
        """
        # Tạo cột họ tên
        df['ho_ten'] = df['Họ đệm'] + ' ' + df['Tên']
        
        # Đổi tên các cột để dễ sử dụng
        column_mapping = {
            'Mã sinh viên': 'mssv',
            'Họ đệm': 'ho_dem',
            'Tên': 'ten',
            'Giới tính': 'gioi_tinh',
            'Ngày sinh': 'ngay_sinh',
            'Lớp': 'lop',
            'Số MH đăng ký': 'so_mh_dk',
            'Số TC đăng ký': 'so_tc_dk',
            'Số MH đạt': 'so_mh_dat',
            'Năm thứ': 'nam_thu', 
            'Số TC tích lũy': 'tc_tich_luy',
            'Ghi chú': 'ghi_chu'
        }
        
        # Xử lý cột điểm tích lũy
        if 'Điểm 4' in df.columns and df.columns.duplicated().any():
            df.columns = pd.Series(df.columns).apply(lambda x: f"{x}_HK" if x in ["Điểm 10", "Điểm 4", "Điểm chữ", "Xếp loại"] else x)
            
            # Tìm cột Điểm 4 tích lũy (cột thứ 17)
            diem4_tich_luy_col = df.columns[16] if len(df.columns) > 16 else None
            
            if diem4_tich_luy_col and 'Điểm 4' in diem4_tich_luy_col:
                df.rename(columns={diem4_tich_luy_col: 'diem_tb'}, inplace=True)
            
            # Xử lý tương tự cho các cột khác
            diem10_tich_luy_col = df.columns[15] if len(df.columns) > 15 else None
            diem_chu_tich_luy_col = df.columns[17] if len(df.columns) > 17 else None
            xep_loai_tich_luy_col = df.columns[18] if len(df.columns) > 18 else None
            
            if diem10_tich_luy_col and 'Điểm 10' in diem10_tich_luy_col:
                df.rename(columns={diem10_tich_luy_col: 'diem_10_tich_luy'}, inplace=True)
            
            if diem_chu_tich_luy_col and 'Điểm chữ' in diem_chu_tich_luy_col:
                df.rename(columns={diem_chu_tich_luy_col: 'diem_chu_tich_luy'}, inplace=True)
            
            if xep_loai_tich_luy_col and 'Xếp loại' in xep_loai_tich_luy_col:
                df.rename(columns={xep_loai_tich_luy_col: 'xep_loai'}, inplace=True)
        
        # Map các cột còn lại
        for new_col, old_cols in column_mapping.items():
            if old_cols in df.columns:
                df.rename(columns={old_cols: new_col}, inplace=True)
        
        # Thêm thông tin khoa từ mã lớp
        df['khoa'] = df['lop'].apply(self._extract_khoa)
        
        # Phân loại sinh viên
        df = self._classify_students(df)
        
        return df
    
    def _extract_khoa(self, lop_name: str) -> str:
        """
        Trích xuất thông tin khoa từ tên lớp
        """
        if pd.isna(lop_name):
            return "Không xác định"
        
        # Mẫu: 11DHTH1, 14DHCNTT, etc.
        parts = re.match(r'(\d+)DH([A-Z]+)', str(lop_name))
        if parts:
            khoa_code = parts.group(2)
            khoa_mapping = {
                'TH': 'Công nghệ thông tin',
                'CNTT': 'Công nghệ thông tin',
                'BM': 'Quản lý thông tin',
                'KT': 'Kinh tế',
                'QT': 'Quản trị',
                'NNA': 'Ngôn ngữ Anh',
                'QTKD': 'Quản trị kinh doanh',
            }
            return khoa_mapping.get(khoa_code, f"Khoa {khoa_code}")
        
        return "Không xác định"
    
    def _normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Chuẩn hóa tên cột dựa trên mapping
        """
        # Tìm các cột tương ứng
        new_columns = {}
        for std_name, possible_names in self.columns_mapping.items():
            for col_name in df.columns:
                if col_name in possible_names:
                    new_columns[col_name] = std_name
                    break
        
        # Đổi tên các cột đã tìm thấy
        df = df.rename(columns=new_columns)
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Làm sạch dữ liệu
        """
        # Xử lý dữ liệu thiếu
        if 'diem_tb' in df.columns:
            df['diem_tb'] = pd.to_numeric(df['diem_tb'], errors='coerce')
            df['diem_tb'].fillna(0, inplace=True)
        
        if 'tc_tich_luy' in df.columns:
            df['tc_tich_luy'] = pd.to_numeric(df['tc_tich_luy'], errors='coerce')
            df['tc_tich_luy'].fillna(0, inplace=True)
        
        # Chuẩn hóa họ tên
        if 'ho_ten' in df.columns:
            df['ho_ten'] = df['ho_ten'].apply(lambda x: str(x).strip().title() if not pd.isna(x) else '')
        
        # Chuẩn hóa mã sinh viên
        if 'mssv' in df.columns:
            df['mssv'] = df['mssv'].astype(str)
        
        return df
    
    def _classify_students(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Phân loại sinh viên dựa trên điểm TB và trạng thái học tập
        """
        # Phân loại theo điểm
        if 'diem_tb' in df.columns:
            conditions = [
                (df['diem_tb'] >= 3.6),
                (df['diem_tb'] >= 3.2),
                (df['diem_tb'] >= 2.5),
                (df['diem_tb'] >= 2.0),
                (df['diem_tb'] >= 1.0),
            ]
            choices = ['Xuất sắc', 'Giỏi', 'Khá', 'Trung bình', 'Yếu']
            df['xep_loai_hoc_luc'] = np.select(conditions, choices, default='Kém')
        
        # Phân loại theo trạng thái học tập
        if 'ghi_chu' in df.columns:
            df['tinh_trang'] = 'Bình thường'
            
            # Tìm các SV cảnh báo
            canh_bao_mask = df['ghi_chu'].astype(str).str.contains('Cảnh báo', case=False, na=False)
            df.loc[canh_bao_mask, 'tinh_trang'] = 'Cảnh báo học vụ'
            
            # Tìm các SV thôi học
            thoi_hoc_mask = df['ghi_chu'].astype(str).str.contains('Thôi học', case=False, na=False)
            df.loc[thoi_hoc_mask, 'tinh_trang'] = 'Thôi học'
        
        # Thêm cột phân loại năm học dựa trên tín chỉ
        if 'tc_tich_luy' in df.columns:
            conditions = [
                (df['tc_tich_luy'] >= 120),
                (df['tc_tich_luy'] >= 90),
                (df['tc_tich_luy'] >= 60),
                (df['tc_tich_luy'] >= 30),
            ]
            choices = ['Năm 4', 'Năm 3', 'Năm 2', 'Năm 1']
            df['nam_hoc'] = np.select(conditions, choices, default='Năm 1')
        
        return df
    
    def _add_analysis_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Thêm các cột phân tích
        """
        # Thêm cột khoa nếu có thông tin lớp
        if 'lop' in df.columns and 'khoa' not in df.columns:
            df['khoa'] = df['lop'].apply(self._extract_khoa)
        
        # Tính toán trạng thái học tập nếu chưa có
        if 'diem_tb' in df.columns and 'tinh_trang' not in df.columns:
            df['tinh_trang'] = 'Bình thường'
            df.loc[df['diem_tb'] < 1.0, 'tinh_trang'] = 'Cảnh báo học vụ'
        
        return df
    
    def get_statistics(self, df: pd.DataFrame) -> dict:
        """
        Tính toán các thống kê từ dữ liệu
        
        Args:
            df: DataFrame dữ liệu sinh viên
            
        Returns:
            Dict chứa các thống kê
        """
        stats = {
            'tong_sinh_vien': len(df)
        }
        
        # Thống kê lớp
        if 'lop' in df.columns:
            stats['so_lop'] = df['lop'].nunique()
        
        # Thống kê khoa
        if 'khoa' in df.columns:
            stats['so_khoa'] = df['khoa'].nunique()
        
        # Thống kê điểm
        if 'diem_tb' in df.columns:
            stats['diem_tb'] = {
                'trung_binh': df['diem_tb'].mean(),
                'cao_nhat': df['diem_tb'].max(),
                'thap_nhat': df['diem_tb'].min()
            }
        
        # Thống kê xếp loại
        if 'xep_loai' in df.columns:
            stats['xep_loai'] = df['xep_loai'].value_counts().to_dict()
        
        # Thống kê theo giới tính
        if 'gioi_tinh' in df.columns:
            stats['gioi_tinh'] = df['gioi_tinh'].value_counts().to_dict()
        
        # Thống kê cảnh báo và thôi học
        if 'tinh_trang' in df.columns:
            stats['canh_bao'] = len(df[df['tinh_trang'] == 'Cảnh báo học vụ'])
            stats['thoi_hoc'] = len(df[df['tinh_trang'] == 'Thôi học'])
        
        return stats
    
    def get_students_at_risk(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Lấy danh sách sinh viên có nguy cơ
        
        Args:
            df: DataFrame dữ liệu sinh viên
            
        Returns:
            DataFrame các sinh viên nguy cơ
        """
        if 'tinh_trang' in df.columns:
            return df[df['tinh_trang'].isin(['Cảnh báo học vụ', 'Thôi học'])]
        
        # Nếu không có cột tinh_trang, dùng điểm để xác định
        if 'diem_tb' in df.columns:
            return df[df['diem_tb'] < 1.0]
        
        return pd.DataFrame()
    
    def get_top_students(self, df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Lấy danh sách sinh viên xuất sắc
        
        Args:
            df: DataFrame dữ liệu sinh viên
            top_n: Số lượng sinh viên muốn lấy
            
        Returns:
            DataFrame các sinh viên xuất sắc
        """
        if 'diem_tb' not in df.columns:
            return pd.DataFrame()
        
        return df.sort_values('diem_tb', ascending=False).head(top_n)
    
    def get_class_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Tính toán thống kê theo lớp
        
        Args:
            df: DataFrame dữ liệu sinh viên
            
        Returns:
            DataFrame thống kê theo lớp
        """
        if 'lop' not in df.columns:
            return pd.DataFrame()
        
        class_stats = df.groupby('lop').agg({
            'mssv': 'count',
            'diem_tb': ['mean', 'max', 'min']
        }).reset_index()
        
        # Làm phẳng MultiIndex columns
        class_stats.columns = ['lop', 'so_sv', 'diem_tb_mean', 'diem_tb_max', 'diem_tb_min']
        
        return class_stats
    
    def get_department_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Tính toán thống kê theo khoa
        
        Args:
            df: DataFrame dữ liệu sinh viên
            
        Returns:
            DataFrame thống kê theo khoa
        """
        if 'khoa' not in df.columns:
            return pd.DataFrame()
        
        dept_stats = df.groupby('khoa').agg({
            'mssv': 'count',
            'diem_tb': ['mean', 'max', 'min']
        }).reset_index()
        
        # Làm phẳng MultiIndex columns
        dept_stats.columns = ['khoa', 'so_sv', 'diem_tb_mean', 'diem_tb_max', 'diem_tb_min']
        
        return dept_stats
