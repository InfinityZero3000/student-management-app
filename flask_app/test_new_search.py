#!/usr/bin/env python3
"""
Test script for new advanced search functionality
"""

import requests
import json

def test_single_mssv_search():
    """Test searching for a single MSSV"""
    print("🔍 Testing single MSSV search...")
    
    url = "http://127.0.0.1:5002/api/advanced-search"
    data = {
        "query": "2033210022"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Success: {result.get('success')}")
    print(f"Total input: {result.get('total_input_items')}")
    print(f"Matches found: {len(result.get('matches', []))}")
    
    if result.get('matches'):
        match = result['matches'][0]
        print(f"Found student: {match.get('Họ đệm', '')} {match.get('Tên', '')}")
        print(f"MSSV: {match.get('Mã sinh viên', '')}")
        print(f"Class: {match.get('Lớp', '')}")
    
    print("-" * 50)

def test_multiple_mssv_search():
    """Test searching for multiple MSSV"""
    print("🔍 Testing multiple MSSV search...")
    
    url = "http://127.0.0.1:5002/api/advanced-search"
    data = {
        "query": """2033210022
2033210184
2033210039"""
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Success: {result.get('success')}")
    print(f"Total input: {result.get('total_input_items')}")
    print(f"Matches found: {len(result.get('matches', []))}")
    
    for i, match in enumerate(result.get('matches', [])[:3]):
        print(f"Match {i+1}: {match.get('Họ đệm', '')} {match.get('Tên', '')} - {match.get('Mã sinh viên', '')}")
    
    print("-" * 50)

def test_name_search():
    """Test searching by name"""
    print("🔍 Testing name search...")
    
    url = "http://127.0.0.1:5002/api/advanced-search"
    data = {
        "query": "Đinh Lê Gia Bảo"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Success: {result.get('success')}")
    print(f"Total input: {result.get('total_input_items')}")
    print(f"Matches found: {len(result.get('matches', []))}")
    
    if result.get('matches'):
        match = result['matches'][0]
        print(f"Found student: {match.get('Họ đệm', '')} {match.get('Tên', '')}")
        print(f"MSSV: {match.get('Mã sinh viên', '')}")
        print(f"Class: {match.get('Lớp', '')}")
    
    print("-" * 50)

def test_class_search():
    """Test searching by class"""
    print("🔍 Testing class search...")
    
    url = "http://127.0.0.1:5002/api/advanced-search"
    data = {
        "query": "12DHBM01"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Success: {result.get('success')}")
    print(f"Total input: {result.get('total_input_items')}")
    print(f"Matches found: {len(result.get('matches', []))}")
    
    if result.get('matches'):
        print(f"First few students from class 12DHBM01:")
        for i, match in enumerate(result.get('matches', [])[:5]):
            print(f"  {i+1}. {match.get('Họ đệm', '')} {match.get('Tên', '')} - {match.get('Mã sinh viên', '')}")
    
    print("-" * 50)

def test_not_found():
    """Test searching for non-existent data"""
    print("🔍 Testing non-existent search...")
    
    url = "http://127.0.0.1:5002/api/advanced-search"
    data = {
        "query": """9999999999
Nguyễn Văn Không Tồn Tại
99DHXXX99"""
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Success: {result.get('success')}")
    print(f"Total input: {result.get('total_input_items')}")
    print(f"Matches found: {len(result.get('matches', []))}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 Testing New Advanced Search Functionality")
    print("=" * 50)
    
    try:
        test_single_mssv_search()
        test_multiple_mssv_search()
        test_name_search()
        test_class_search()
        test_not_found()
        
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
