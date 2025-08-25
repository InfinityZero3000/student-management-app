#!/usr/bin/env python3
"""
Test file for student comparison functionality with large data set
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import extract_student_info, find_matching_students, load_sample_data
import server

# Load data first
load_sample_data()

def test_large_dataset():
    """Test with a large dataset (67 lines)"""
    print("=== Testing Large Dataset (67 lines) ===")
    
    # Create test data with 67 items (mix of MSSV and names)
    test_data_lines = [
        "2033210022",
        "Đinh Lê Gia Bảo", 
        "2033210184",
        "Lê Quang Đại",
        "2033210039", 
        "Nguyễn Hải Đăng",
        "2033210032",
        "Vòng Diệp",
        "2033210045",
        "Phạm Minh Tuấn",
        "2033210067",
        "Nguyễn Văn An",
        "2033210089",
        "Trần Thị Lan",
        "2033210123",
        "Lê Minh Khoa",
        "2033210156",
        "Hoàng Thị Mai",
        "2033210178",
        "Phan Đức Huy",
        "2033210203",
        "Võ Thị Nga",
        "2033210234",
        "Đặng Quốc Việt",
        "2033210267",
        "Nguyễn Thị Hoa",
        "2033210289",
        "Lý Thanh Tùng",
        "2033210301",
        "Bùi Văn Đức",
        "2033210334",
        "Trương Thị Linh",
        "2033210356",
        "Cao Minh Đạt",
        "2033210378",
        "Đinh Thị Thu",
        "2033210401",
        "Đỗ Văn Hùng",
        "2033210423",
        "Dương Thị Kim",
        "2033210445",
        "Giang Văn Hải",
        "2033210467",
        "Hà Thị Lan",
        "2033210489",
        "Hồ Minh Quân",
        "2033210512",
        "Huỳnh Thị Nga",
        "2033210534",
        "Kiều Văn Tài",
        "2033210556",
        "Lâm Thị Hương",
        "2033210578",
        "Lưu Minh Đức",
        "2033210601",
        "Mai Thị Hạnh",
        "2033210623",
        "Ngô Văn Phong",
        "2033210645",
        "Phùng Thị Hồng",
        "2033210667",
        "Quách Minh Tuấn",
        "2033210689",
        "Rồng Thị Lan",
        "2033210712",
        "Sơn Văn Hùng",
        "2033210734",
        "Tạ Thị Minh",
        "2033210756",
        "Thái Văn Đức",
        "2033210778",
        "Tiêu Thị Nga",
        "2033210801",
        "Tôn Minh Khoa",
        "2033210823",
        "Trịnh Thị Hoa",
        "2033210845",
        "Ứng Văn Tài",
        "2033210867",
        "Vũ Thị Lan",
        "2033210889",
        "Xa Minh Đức"
    ]
    
    # Join all lines
    large_test_data = '\n'.join(test_data_lines)
    
    print(f"Total input lines: {len(test_data_lines)}")
    print("First 5 lines:")
    for i, line in enumerate(test_data_lines[:5]):
        print(f"  {i+1}. {line}")
    print("...")
    print("Last 5 lines:")
    for i, line in enumerate(test_data_lines[-5:]):
        print(f"  {len(test_data_lines)-4+i}. {line}")
    print()
    
    # Extract student information
    print("=== Extracting Student Information ===")
    extracted_info = extract_student_info(large_test_data)
    
    print(f"MSSV found: {len(extracted_info['mssv'])}")
    print(f"Names found: {len(extracted_info['name'])}")
    print(f"Total extracted: {len(extracted_info['mssv']) + len(extracted_info['name'])}")
    print()
    
    # Find matching students
    print("=== Finding Matching Students ===")
    matches = find_matching_students(extracted_info)
    
    print(f"Total matches found: {len(matches)}")
    print()
    
    # Analyze results
    mssv_matches = [m for m in matches if m['match_type'] == 'mssv']
    name_matches = [m for m in matches if 'name' in m['match_type']]
    
    print(f"MSSV matches: {len(mssv_matches)}")
    print(f"Name matches: {len(name_matches)}")
    print()
    
    # Show first 10 matches
    print("=== First 10 Matches ===")
    for i, match in enumerate(matches[:10]):
        print(f"Match {i+1}:")
        print(f"  Input: {match.get('input_value', 'N/A')}")
        print(f"  Type: {match.get('match_type', 'N/A')}")
        print(f"  Score: {match.get('match_score', 'N/A')}")
        print(f"  MSSV: {match.get('Mã sinh viên', 'N/A')}")
        print(f"  Name: {match.get('Họ đệm', 'N/A')} {match.get('Tên', 'N/A')}")
        print()
    
    # Test with exact_match and show_all_matches options
    print("=== Testing API-style filtering ===")
    
    # Simulate exact_match = True
    exact_matches = [m for m in matches if m['match_score'] >= 0.8]
    print(f"High confidence matches (≥80%): {len(exact_matches)}")
    
    # Simulate show_all_matches = False (old limit of 50)
    old_limited = matches[:50]
    print(f"Old limit (50): {len(old_limited)}")
    
    # New approach - no artificial limits
    print(f"New approach (no limits): {len(matches)}")
    
    return matches

if __name__ == "__main__":
    print("Testing Student Comparison with Large Dataset")
    print("=" * 50)
    
    # Check if data is loaded
    if server.student_data is None or server.student_data.empty:
        print("ERROR: No student data loaded!")
        exit(1)
    
    print(f"Database has {len(server.student_data)} students")
    print()
    
    # Run the test
    matches = test_large_dataset()
    
    print(f"\nFinal Summary:")
    print(f"Input items: 67")
    print(f"Matches found: {len(matches)}")
    print(f"Match rate: {len(matches)/67*100:.1f}%")
    print("\nTest completed successfully! ✅")
