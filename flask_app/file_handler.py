"""
Module xử lý file đầu vào và xuất cải tiến
Hỗ trợ đầy đủ các định dạng file của HUIT
"""

import pandas as pd
import numpy as np
import io
import os
import re
import json
import csv
from typing import Union, BinaryIO, Optional, Dict, List, Any
import streamlit as st
from datetime import datetime
import base64

class FileHandler:
    """Class xử lý các file đầu vào và xuất"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json']
        self.encoding_list = ['utf-8-sig', 'utf-8', 'cp1252', 'latin1', 'gb2312']
        self.backup_folder = "backups"
        
        # Đảm bảo thư mục backup tồn tại
        os.makedirs(self.backup_folder, exist_ok=True)
    
    def read_csv_file(self, file_input: Union[str, BinaryIO]) -> pd.DataFrame:
        """
        Đọc file CSV với encoding tự động detect
        
        Args:
            file_input: Đường dẫn file hoặc file object từ Streamlit
            
        Returns:
            DataFrame chứa dữ liệu
        """
        try:
            # Nếu là file object từ Streamlit
            if hasattr(file_input, 'read'):
                # Đọc nội dung file
                content = file_input.read()
                
                # Thử từng encoding
                for encoding in self.encoding_list:
                    try:
                        # Decode content với encoding
                        text_content = content.decode(encoding)
                        
                        # Tạo StringIO object
                        string_io = io.StringIO(text_content)
                        
                        # Đọc CSV
                        df = pd.read_csv(string_io)
                        
                        # Kiểm tra dữ liệu hợp lệ
                        if not df.empty and len(df.columns) > 1:
                            return df
                    except Exception:
                        continue
                
                # Nếu không đọc được, báo lỗi
                st.error("[x-circle] Không thể đọc file CSV với các encoding thông dụng")
                return pd.DataFrame()
            
            # Nếu là đường dẫn file
            else:
                # Thử từng encoding
                for encoding in self.encoding_list:
                    try:
                        df = pd.read_csv(file_input, encoding=encoding)
                        
                        # Kiểm tra dữ liệu hợp lệ
                        if not df.empty and len(df.columns) > 1:
                            return df
                    except Exception:
                        continue
                
                # Nếu không đọc được, báo lỗi
                st.error(f"[x-circle] Không thể đọc file {file_input} với các encoding thông dụng")
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"[x-circle] Lỗi đọc file CSV: {str(e)}")
            return pd.DataFrame()
    
    def read_excel_file(self, file_input: Union[str, BinaryIO]) -> pd.DataFrame:
        """
        Đọc file Excel
        
        Args:
            file_input: Đường dẫn file hoặc file object từ Streamlit
            
        Returns:
            DataFrame chứa dữ liệu
        """
        try:
            if hasattr(file_input, 'read'):
                df = pd.read_excel(file_input)
            else:
                df = pd.read_excel(file_input)
            
            return df
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi đọc file Excel: {str(e)}")
            return pd.DataFrame()
    
    def read_file(self, file_input: Union[str, BinaryIO]) -> pd.DataFrame:
        """
        Đọc file dữ liệu (tự động phát hiện định dạng)
        
        Args:
            file_input: Đường dẫn file hoặc file object từ Streamlit
            
        Returns:
            DataFrame chứa dữ liệu
        """
        try:
            # Lấy phần mở rộng của file
            if hasattr(file_input, 'name'):
                file_name = file_input.name
            else:
                file_name = file_input
                
            file_extension = os.path.splitext(file_name)[1].lower()
            
            # Đọc file theo định dạng
            if file_extension in ['.csv']:
                return self.read_csv_file(file_input)
                
            elif file_extension in ['.xlsx', '.xls']:
                return self.read_excel_file(file_input)
                
            elif file_extension in ['.json']:
                return self.read_json_file(file_input)
                
            else:
                st.error(f"[x-circle] Định dạng file {file_extension} không được hỗ trợ")
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"[x-circle] Lỗi đọc file: {str(e)}")
            return pd.DataFrame()
    
    def read_huit_student_data(self, file_input: Union[str, BinaryIO]) -> pd.DataFrame:
        """
        Đọc dữ liệu sinh viên từ định dạng đặc thù của HUIT
        
        Args:
            file_input: Đường dẫn file hoặc file object từ Streamlit
            
        Returns:
            DataFrame chứa dữ liệu
        """
        try:
            # Đọc file
            df = self.read_file(file_input)
            
            # Kiểm tra xem có phải định dạng của HUIT không
            if "Mã sinh viên" in df.columns and "Họ đệm" in df.columns and "Tên" in df.columns:
                return df
            else:
                st.warning("[alert-triangle] File không đúng định dạng dữ liệu sinh viên HUIT")
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"[x-circle] Lỗi đọc dữ liệu sinh viên HUIT: {str(e)}")
            return pd.DataFrame()
    
    def read_json_file(self, file_input: Union[str, BinaryIO]) -> pd.DataFrame:
        """
        Đọc file JSON
        
        Args:
            file_input: Đường dẫn file hoặc file object từ Streamlit
            
        Returns:
            DataFrame chứa dữ liệu
        """
        try:
            if hasattr(file_input, 'read'):
                content = file_input.read()
                data = json.loads(content)
            else:
                with open(file_input, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # Chuyển đổi JSON thành DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Nếu là dict, thử xem có phải định dạng dataset_stats.json không
                if "statistics" in data and isinstance(data["statistics"], dict):
                    stats = data["statistics"]
                    df = pd.DataFrame([stats])
                else:
                    df = pd.DataFrame([data])
            else:
                st.error("[x-circle] Định dạng JSON không đúng cấu trúc")
                return pd.DataFrame()
                
            return df
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi đọc file JSON: {str(e)}")
            return pd.DataFrame()
    
    def export_to_excel(self, df: pd.DataFrame, filename: str) -> bytes:
        """
        Xuất DataFrame ra file Excel
        
        Args:
            df: DataFrame cần xuất
            filename: Tên file xuất
            
        Returns:
            Dữ liệu Excel dạng bytes
        """
        try:
            # Tạo buffer để lưu Excel
            output = io.BytesIO()
            
            # Tạo ExcelWriter
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Data')
                
                # Định dạng worksheet
                workbook = writer.book
                worksheet = writer.sheets['Data']
                
                # Định dạng tiêu đề
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1
                })
                
                # Áp dụng định dạng cho tiêu đề
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    
                # Điều chỉnh chiều rộng cột
                for i, col in enumerate(df.columns):
                    max_len = max(
                        df[col].astype(str).map(len).max(),  # Độ dài giá trị lớn nhất
                        len(str(col))  # Độ dài tiêu đề
                    ) + 2  # Thêm padding
                    worksheet.set_column(i, i, max_len)
            
            # Lấy dữ liệu từ buffer
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi xuất Excel: {str(e)}")
            return b''
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """
        Xuất DataFrame ra file CSV
        
        Args:
            df: DataFrame cần xuất
            filename: Tên file xuất
            
        Returns:
            Nội dung CSV
        """
        try:
            # Tạo CSV trong buffer
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            
            # Lấy nội dung CSV
            csv_str = csv_buffer.getvalue()
            return csv_str
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi xuất CSV: {str(e)}")
            return ""
    
    def export_to_json(self, df: pd.DataFrame, filename: str) -> str:
        """
        Xuất DataFrame ra file JSON
        
        Args:
            df: DataFrame cần xuất
            filename: Tên file xuất
            
        Returns:
            Nội dung JSON
        """
        try:
            # Chuyển đổi DataFrame thành JSON
            json_str = df.to_json(orient='records', force_ascii=False)
            return json_str
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi xuất JSON: {str(e)}")
            return ""
    
    def create_backup(self, df: pd.DataFrame) -> bool:
        """
        Tạo bản backup của dữ liệu
        
        Args:
            df: DataFrame cần backup
            
        Returns:
            True nếu thành công, False nếu thất bại
        """
        try:
            # Tạo tên file với timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.csv"
            backup_path = os.path.join(self.backup_folder, backup_filename)
            
            # Lưu file
            df.to_csv(backup_path, index=False, encoding='utf-8-sig')
            
            return True
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi tạo backup: {str(e)}")
            return False
    
    def list_backups(self) -> List[str]:
        """
        Liệt kê các bản backup
        
        Returns:
            Danh sách tên file backup
        """
        try:
            # Liệt kê các file trong thư mục backup
            files = os.listdir(self.backup_folder)
            
            # Lọc ra các file CSV backup
            backup_files = [f for f in files if f.startswith('backup_') and f.endswith('.csv')]
            
            # Sắp xếp theo thời gian (mới nhất lên đầu)
            backup_files.sort(reverse=True)
            
            return backup_files
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi liệt kê backup: {str(e)}")
            return []
    
    def restore_from_backup(self, backup_filename: str) -> pd.DataFrame:
        """
        Khôi phục từ bản backup
        
        Args:
            backup_filename: Tên file backup
            
        Returns:
            DataFrame từ bản backup
        """
        try:
            backup_path = os.path.join(self.backup_folder, backup_filename)
            
            # Đọc file CSV backup
            df = pd.read_csv(backup_path, encoding='utf-8-sig')
            
            return df
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi khôi phục backup: {str(e)}")
            return pd.DataFrame()
    
    def generate_html_report(self, df: pd.DataFrame, title: str, 
                           summary: Dict[str, Any] = None) -> str:
        """
        Tạo báo cáo HTML từ DataFrame
        
        Args:
            df: DataFrame cần xuất
            title: Tiêu đề báo cáo
            summary: Dict chứa thông tin tổng hợp (optional)
            
        Returns:
            Nội dung HTML của báo cáo
        """
        try:
            # Khởi tạo HTML
            html = f"""
            <!DOCTYPE html>
            <html lang="vi">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 20px;
                        color: #333;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #1e40af, #3b82f6);
                        color: white;
                        padding: 20px;
                        border-radius: 10px 10px 0 0;
                        margin-bottom: 20px;
                    }}
                    h1 {{
                        margin: 0;
                        font-size: 24px;
                    }}
                    .datetime {{
                        font-size: 14px;
                        margin-top: 5px;
                        opacity: 0.8;
                    }}
                    .summary {{
                        background-color: #f8fafc;
                        border: 1px solid #e2e8f0;
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 20px;
                    }}
                    .summary-title {{
                        font-weight: 600;
                        margin-bottom: 10px;
                        color: #1e40af;
                    }}
                    .summary-grid {{
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                        gap: 15px;
                    }}
                    .summary-item {{
                        background: white;
                        border: 1px solid #e2e8f0;
                        border-radius: 8px;
                        padding: 12px;
                    }}
                    .item-label {{
                        font-size: 13px;
                        color: #64748b;
                        margin-bottom: 5px;
                    }}
                    .item-value {{
                        font-size: 18px;
                        font-weight: 600;
                        color: #1e293b;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }}
                    th {{
                        background-color: #f1f5f9;
                        padding: 12px 15px;
                        text-align: left;
                        font-weight: 600;
                        border-bottom: 2px solid #e2e8f0;
                    }}
                    td {{
                        padding: 10px 15px;
                        border-bottom: 1px solid #e2e8f0;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f8fafc;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        color: #64748b;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>{title}</h1>
                        <div class="datetime">Thời gian tạo: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>
                    </div>
            """
            
            # Thêm phần tóm tắt nếu có
            if summary:
                html += """
                    <div class="summary">
                        <div class="summary-title">Thông tin tổng hợp</div>
                        <div class="summary-grid">
                """
                
                for key, value in summary.items():
                    if isinstance(value, dict):
                        continue
                    
                    label = key.replace('_', ' ').title()
                    html += f"""
                            <div class="summary-item">
                                <div class="item-label">{label}</div>
                                <div class="item-value">{value}</div>
                            </div>
                    """
                
                html += """
                        </div>
                    </div>
                """
            
            # Thêm bảng dữ liệu
            html += """
                    <table>
                        <thead>
                            <tr>
            """
            
            # Thêm tiêu đề cột
            for col in df.columns:
                html += f"<th>{col}</th>"
            
            html += """
                            </tr>
                        </thead>
                        <tbody>
            """
            
            # Thêm dữ liệu
            for _, row in df.iterrows():
                html += "<tr>"
                for col in df.columns:
                    html += f"<td>{row[col]}</td>"
                html += "</tr>"
            
            html += """
                        </tbody>
                    </table>
                    
                    <div class="footer">
                        Báo cáo được tạo từ Ứng dụng Quản lý Sinh viên HUIT
                    </div>
                </div>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            st.error(f"[x-circle] Lỗi tạo báo cáo HTML: {str(e)}")
            return ""
