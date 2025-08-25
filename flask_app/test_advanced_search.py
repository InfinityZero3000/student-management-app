"""
Test script for Advanced Search functionality
"""

import requests
import json

# Test data - Mix of MSSV, names, and other info
test_data = """
2033210022
Nguyễn Văn An
2033210023
Lê Thị Bình
14TCLC3
01/01/2000
Trần Minh Châu
2033210024
"""

def test_advanced_search_text():
    """Test advanced search with text input"""
    url = "http://127.0.0.1:5002/api/advanced-search"
    
    payload = {
        "query": test_data,
        "exact_match_only": True,
        "include_partial_match": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Advanced Search Test - SUCCESS")
            print(f"📊 Total input items: {result.get('total_input_items', 0)}")
            print(f"🎯 Matches found: {len(result.get('matches', []))}")
            
            # Show extracted data
            extracted = result.get('extracted_data', {})
            print(f"🔍 Extracted data:")
            print(f"   - MSSV: {len(extracted.get('mssv', []))} items")
            print(f"   - Names: {len(extracted.get('names', []))} items")
            print(f"   - Classes: {len(extracted.get('classes', []))} items")
            print(f"   - Dates: {len(extracted.get('dates', []))} items")
            
            # Show some matches
            matches = result.get('matches', [])
            if matches:
                print(f"\n📝 Sample matches:")
                for i, match in enumerate(matches[:3]):
                    score = match.get('match_score', 0)
                    input_val = match.get('input_value', 'N/A')
                    match_type = match.get('match_type', 'N/A')
                    
                    # Try to get student name and MSSV
                    student_name = "N/A"
                    student_mssv = "N/A"
                    
                    for key, value in match.items():
                        if 'tên' in key.lower() or 'name' in key.lower():
                            student_name = value
                        elif 'mssv' in key.lower() or 'id' in key.lower():
                            student_mssv = str(value).replace('.0', '')
                    
                    print(f"   {i+1}. Input: '{input_val}' → Match: {student_name} ({student_mssv}) | Score: {score:.2f} | Type: {match_type}")
            
        else:
            print(f"❌ Advanced Search Test - FAILED")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Advanced Search Test - ERROR: {e}")

def test_simple_searches():
    """Test simple individual searches"""
    simple_tests = [
        "2033210022",
        "Nguyễn Văn An", 
        "14TCLC3",
        "01/01/2000"
    ]
    
    print(f"\n🧪 Testing simple searches...")
    
    for test_input in simple_tests:
        url = "http://127.0.0.1:5002/api/advanced-search"
        
        payload = {
            "query": test_input,
            "exact_match_only": True,
            "include_partial_match": True
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                matches = result.get('matches', [])
                extracted = result.get('extracted_data', {})
                
                total_extracted = sum(len(v) for v in extracted.values() if isinstance(v, list))
                
                print(f"   📍 '{test_input}' → Extracted: {total_extracted}, Matches: {len(matches)}")
                
            else:
                print(f"   ❌ '{test_input}' → Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ '{test_input}' → Exception: {e}")

if __name__ == "__main__":
    print("🚀 Testing Advanced Search Functionality")
    print("=" * 50)
    
    test_advanced_search_text()
    test_simple_searches()
    
    print("\n✨ Test completed!")
