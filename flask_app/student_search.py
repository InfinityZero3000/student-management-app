"""
Student Search Engine for HUIT Management System
Advanced student search algorithms with exact matching
Handles MSSV, name, class, and date-based searches
"""

import pandas as pd
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

def identify_database_columns(student_data):
    """Identify important columns in the database"""
    if student_data is None:
        return {}
    
    columns = {
        'mssv': [],
        'ho_dem': [],
        'ten': [],
        'full_name': [],
        'class': [],
        'birth_date': [],
        'score': [],
        'rank': []
    }
    
    for col in student_data.columns:
        col_lower = col.lower().replace(' ', '_')
        
        if any(keyword in col_lower for keyword in ['mssv', 'id', 'ma_sv', 'student_id', 'mã_sinh_viên']):
            columns['mssv'].append(col)
        elif 'họ_đệm' in col_lower or 'ho_dem' in col_lower:
            columns['ho_dem'].append(col)
        elif col_lower in ['tên', 'ten']:
            columns['ten'].append(col)
        elif any(keyword in col_lower for keyword in ['họ_và_tên', 'ho_va_ten', 'fullname', 'full_name']):
            columns['full_name'].append(col)
        elif any(keyword in col_lower for keyword in ['lớp', 'lop', 'class']):
            columns['class'].append(col)
        elif any(keyword in col_lower for keyword in ['ngày_sinh', 'ngay_sinh', 'birth_date', 'dob']):
            columns['birth_date'].append(col)
        elif any(keyword in col_lower for keyword in ['điểm', 'diem', 'score', 'point']):
            columns['score'].append(col)
        elif any(keyword in col_lower for keyword in ['xếp_loại', 'xep_loai', 'rank', 'grade']):
            columns['rank'].append(col)
    
    return columns

def search_by_mssv(mssv, student_data, db_columns):
    """Search student by MSSV - exact match only"""
    matches = []
    mssv_clean = str(mssv).strip()
    
    for mssv_col in db_columns.get('mssv', []):
        for idx, student in student_data.iterrows():
            student_mssv = str(student[mssv_col]).replace('.0', '').strip()
            
            if student_mssv == mssv_clean:
                student_info = student.to_dict()
                student_info['input_value'] = mssv
                student_info['match_field'] = mssv_col
                
                matches.append(student_info)
                break  # Found exact match, stop searching
    
    return matches

def search_by_name(name, student_data, db_columns):
    """Search student by name - exact match only for precision"""
    matches = []
    name_clean = str(name).strip().lower()
    
    for idx, student in student_data.iterrows():
        # Try full name columns first
        for full_name_col in db_columns.get('full_name', []):
            if full_name_col in student.index:
                student_name = str(student[full_name_col]).strip().lower()
                
                if student_name == name_clean:
                    # Exact match
                    student_info = student.to_dict()
                    student_info['input_value'] = name
                    student_info['match_field'] = full_name_col
                    
                    matches.append(student_info)
                    break
        
        # If not found in full name, try combining ho_dem + ten
        if not any(match['input_value'] == name for match in matches if 'input_value' in match):
            ho_dem_cols = db_columns.get('ho_dem', [])
            ten_cols = db_columns.get('ten', [])
            
            if ho_dem_cols and ten_cols:
                ho_dem = str(student[ho_dem_cols[0]]).strip() if ho_dem_cols[0] in student.index else ''
                ten = str(student[ten_cols[0]]).strip() if ten_cols[0] in student.index else ''
                full_name = f"{ho_dem} {ten}".strip().lower()
                
                if full_name == name_clean:
                    student_info = student.to_dict()
                    student_info['input_value'] = name
                    student_info['match_field'] = f"{ho_dem_cols[0]}+{ten_cols[0]}"
                    
                    matches.append(student_info)
    
    return matches

def search_by_class(class_name, student_data, db_columns):
    """Search students by class - exact match only"""
    matches = []
    class_clean = str(class_name).strip().lower()
    
    for class_col in db_columns.get('class', []):
        for idx, student in student_data.iterrows():
            if class_col in student.index:
                student_class = str(student[class_col]).strip().lower()
                
                if student_class == class_clean:
                    student_info = student.to_dict()
                    student_info['input_value'] = class_name
                    student_info['match_field'] = class_col
                    
                    matches.append(student_info)
    
    return matches

def parse_date_string(date_str):
    """Parse date string in various formats"""
    if not date_str or str(date_str).strip() in ['', 'nan', 'NaT']:
        return None
    
    date_str = str(date_str).strip()
    
    # Common date formats
    formats = [
        '%d/%m/%Y',
        '%m/%d/%Y', 
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%Y/%m/%d'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None

def search_by_date(date_str, student_data, db_columns):
    """Search students by birth date - exact match only"""
    matches = []
    
    # Try to parse the date in various formats
    parsed_date = parse_date_string(date_str)
    if not parsed_date:
        return matches
    
    for date_col in db_columns.get('birth_date', []):
        for idx, student in student_data.iterrows():
            if date_col in student.index:
                student_date = parse_date_string(str(student[date_col]))
                
                if student_date and student_date == parsed_date:
                    student_info = student.to_dict()
                    student_info['input_value'] = date_str
                    student_info['match_field'] = date_col
                    
                    matches.append(student_info)
    
    return matches

def determine_input_type(input_text):
    """Determine what type of input this is"""
    input_text = str(input_text).strip()
    
    # Check if it's MSSV (all digits, usually 6-10 characters)
    if input_text.isdigit() and 6 <= len(input_text) <= 10:
        return 'mssv'
    
    # Check if it's a date (contains /, -)
    if re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', input_text):
        return 'date'
    
    # Check if it's a class (contains digits and letters, short)
    if re.search(r'^\d+[A-Za-z]+\d*$', input_text) and len(input_text) <= 15:
        return 'class'
    
    # Default to name
    return 'name'

def advanced_student_search(input_list, student_data):
    """
    Thực hiện tìm kiếm nâng cao từ danh sách đầu vào - GIỮ THỨ TỰ INPUT
    """
    if student_data is None or student_data.empty:
        return []
        
    # Xác định cấu trúc cột
    db_columns = identify_database_columns(student_data)
    
    # Log thông tin
    logger.info(f"Processing {len(input_list)} input items in order")
    
    # Kết quả tìm kiếm theo thứ tự
    ordered_results = []
    
    # Xử lý từng dòng đầu vào THEO THỨ TỰ
    for input_index, input_text in enumerate(input_list):
        if not input_text.strip():
            continue
            
        # Xác định loại đầu vào: MSSV, tên, lớp, ngày sinh
        input_type = determine_input_type(input_text)
        
        # Tìm kiếm theo loại
        matches = []
        if input_type == 'mssv':
            matches = search_by_mssv(input_text, student_data, db_columns)
        elif input_type == 'name':
            matches = search_by_name(input_text, student_data, db_columns)
        elif input_type == 'class':
            matches = search_by_class(input_text, student_data, db_columns)
        elif input_type == 'date':
            matches = search_by_date(input_text, student_data, db_columns)
        else:
            # Tìm theo tất cả các loại
            matches.extend(search_by_mssv(input_text, student_data, db_columns))
            if not matches:
                matches.extend(search_by_name(input_text, student_data, db_columns))
            if not matches:
                matches.extend(search_by_class(input_text, student_data, db_columns))
            if not matches:
                matches.extend(search_by_date(input_text, student_data, db_columns))
        
        # Thêm thông tin về thứ tự và input vào kết quả
        for match in matches:
            if isinstance(match, dict):
                match['input_value'] = input_text
                match['input_order'] = input_index  # Thêm thứ tự input
                match['match_score'] = 1.0  # Exact match score
                
        # Thêm vào kết quả theo thứ tự (chỉ lấy match đầu tiên nếu có nhiều)
        if matches:
            ordered_results.append(matches[0])  # Chỉ lấy kết quả tốt nhất
    
    # Log kết quả
    logger.info(f"Returning {len(ordered_results)} results in input order")
    
    # Trả về kết quả đã được sắp xếp theo thứ tự input
    return ordered_results