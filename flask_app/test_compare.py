#!/usr/bin/env python3
"""
Test file for student comparison functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import extract_student_info, find_matching_students, load_sample_data, student_data
import pandas as pd

# Load data first
load_sample_data()

def test_extract_student_info():
    """Test the student info extraction function"""
    print("=== Testing extract_student_info ===")
    
    # Test case 1: Simple MSSV
    test_text1 = "2033210022"
    result1 = extract_student_info(test_text1)
    print(f"Test 1 - Input: '{test_text1}'")
    print(f"Result: {result1}")
    print()
    
    # Test case 2: Simple name
    test_text2 = "Đinh Lê Gia Bảo"
    result2 = extract_student_info(test_text2)
    print(f"Test 2 - Input: '{test_text2}'")
    print(f"Result: {result2}")
    print()
    
    # Test case 3: Mixed input
    test_text3 = """2033210022
Đinh Lê Gia Bảo
2033210184
Lê Quang Đại"""
    result3 = extract_student_info(test_text3)
    print(f"Test 3 - Input: '{test_text3}'")
    print(f"Result: {result3}")
    print()
    
    return result3

def test_find_matching_students():
    """Test the student matching function"""
    print("=== Testing find_matching_students ===")
    
    # Import and access the global student_data from server module
    import server
    
    if server.student_data is None or server.student_data.empty:
        print("No student data loaded!")
        return
    
    print(f"Student data shape: {server.student_data.shape}")
    print(f"Columns: {list(server.student_data.columns)}")
    print()
    
    # Test with extracted info
    extracted_info = {
        'mssv': {'2033210022', '2033210184'},
        'name': {'Đinh Lê Gia Bảo', 'Lê Quang Đại'}
    }
    
    print(f"Testing with extracted info: {extracted_info}")
    matches = find_matching_students(extracted_info)
    print(f"Found {len(matches)} matches:")
    
    for i, match in enumerate(matches):
        print(f"\nMatch {i+1}:")
        print(f"  Score: {match.get('match_score', 'N/A')}")
        print(f"  Type: {match.get('match_type', 'N/A')}")
        print(f"  Input: {match.get('input_value', 'N/A')}")
        print(f"  MSSV: {match.get('Mã sinh viên', 'N/A')}")
        print(f"  Name: {match.get('Họ đệm', 'N/A')} {match.get('Tên', 'N/A')}")
        print(f"  Class: {match.get('Lớp', 'N/A')}")
        print(f"  Score: {match.get('Điểm 10', 'N/A')}")

if __name__ == "__main__":
    print("Testing Student Comparison Features")
    print("====================================")
    
    # Test extraction
    extracted_info = test_extract_student_info()
    
    # Test matching
    test_find_matching_students()
    
    print("\nTest completed!")
