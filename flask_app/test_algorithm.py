#!/usr/bin/env python3
"""
Test script để kiểm tra thuật toán extract_student_info đã cải thiện
"""

import re
import unicodedata
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_student_info(text):
    """Extract student names and IDs from text - OPTIMIZED for precision"""
    import unicodedata
    
    # Normalize text - remove special chars, extra spaces  
    normalized_text = unicodedata.normalize('NFKD', text)
    
    extracted_info = {'mssv': set(), 'name': set()}
    
    # Split text into lines and process each line individually
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    
    logger.info(f"Processing {len(lines)} lines of input text")
    
    for line_idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        logger.debug(f"Processing line {line_idx + 1}: '{line}'")
        
        # Strategy 1: Check if entire line is a student ID
        if line.isdigit() and 6 <= len(line) <= 10:
            # Additional validation for Vietnamese student ID patterns
            if (len(line) == 8 and line.startswith('20')) or \
               (len(line) == 10 and line.startswith('20')) or \
               (6 <= len(line) <= 10):
                extracted_info['mssv'].add(line)
                logger.debug(f"Found MSSV: {line}")
                continue
        
        # Strategy 2: Check if entire line is a Vietnamese name
        words = line.split()
        logger.debug(f"Line '{line}': {len(words)} words, length {len(line)}")
        
        if (len(words) >= 2 and  # At least 2 words (first name + last name)
            len(words) <= 5 and  # Not more than 5 words 
            not any(char.isdigit() for char in line) and  # No digits
            5 <= len(line) <= 40 and  # Reasonable length
            all(len(word) >= 1 for word in words) and  # Each word at least 1 char (allowing single letter names)
            not any(word.lower() in ['file', 'data', 'csv', 'excel', 'document', 'text'] for word in words)):  # No tech words
            
            # Check for Vietnamese name characteristics
            has_vietnamese_chars = any(char in 'àáâãèéêìíòóôõùúăđĩũơưăạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵýỷỹ' for char in line.lower())
            has_proper_caps = all(word[0].isupper() and (len(word) == 1 or word[1:].islower()) for word in words)
            is_all_caps = all(word.isupper() for word in words)
            
            # Also check for common Vietnamese names patterns
            has_common_vn_chars = any(char in 'ă ô ư đ' for char in line.lower())
            
            logger.debug(f"Name checks - vn_chars: {has_vietnamese_chars}, proper_caps: {has_proper_caps}, all_caps: {is_all_caps}, common_vn: {has_common_vn_chars}")
            
            if has_vietnamese_chars or has_proper_caps or is_all_caps or has_common_vn_chars:
                extracted_info['name'].add(line)
                logger.debug(f"Found name: {line}")
                continue
        else:
            logger.debug(f"Line '{line}' failed basic name criteria")
        
        # Strategy 3: Look for patterns within the line (for mixed content)
        # MSSV patterns (more restrictive)
        mssv_patterns = [
            r'\b(20\d{8})\b',      # 10-digit starting with 20
            r'\b(20\d{6})\b',      # 8-digit starting with 20  
            r'\b(\d{6,10})\b'      # General 6-10 digit pattern
        ]
        
        for pattern in mssv_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                if 6 <= len(match) <= 10:
                    extracted_info['mssv'].add(match)
                    logger.debug(f"Found MSSV in line: {match}")
        
        # Name patterns within line (more restrictive)
        # Only look for names if the line contains mixed content
        if any(char.isdigit() for char in line):  # Mixed content
            name_pattern = r'\b([A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸ][a-zàáâãèéêìíòóôõùúăđĩũơưăạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵýỷỹ]+(?:\s+[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸ][a-zàáâãèéêìíòóôõùúăđĩũơưăạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵýỷỹ]+)+)\b'
            name_matches = re.findall(name_pattern, line)
            for match in name_matches:
                words = match.split()
                if (2 <= len(words) <= 5 and
                    5 <= len(match) <= 40 and
                    all(len(word) >= 2 for word in words)):
                    extracted_info['name'].add(match)
                    logger.debug(f"Found name in mixed line: {match}")
    
    logger.info(f"Extraction complete - MSSV: {len(extracted_info['mssv'])}, Names: {len(extracted_info['name'])}")
    logger.debug(f"MSVs found: {list(extracted_info['mssv'])}")
    logger.debug(f"Names found: {list(extracted_info['name'])}")
    
    return extracted_info

if __name__ == "__main__":
    # Test với các input khác nhau
    test_cases = [
        "2033210022",  # 1 MSSV
        "2033210022\nNguyễn Văn A\n2033210023",  # 2 MSSV + 1 tên
        "Nguyễn Văn A\nTrần Thị B",  # 2 tên
        "2033210022 Nguyễn Văn A\n2033210023 Trần Thị B",  # Mixed content
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n=== TEST CASE {i} ===")
        print(f"Input: {repr(test_input)}")
        result = extract_student_info(test_input)
        total = len(result['mssv']) + len(result['name'])
        print(f"Result: {total} items total (MSSV: {len(result['mssv'])}, Names: {len(result['name'])})")
        print(f"MSVs: {list(result['mssv'])}")
        print(f"Names: {list(result['name'])}")
