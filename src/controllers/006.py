# test_merge_file_info.py
import json
from pack_init_file import merge_file_info  # Assuming the original file is named merge_file_info.py

def test_merge_file_info():
    # Test case 1: Basic merge with different keys
    info1 = {
        "file_name": "校园安全手册 (2024版).pdf",
        "new_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
    }
    
    info2 = {
        "name": "校园安全手册 (2024版)",
        "extension": ".pdf",
    }
    
    result = merge_file_info(info1, info2)
    expected = {
        "file_name": "校园安全手册 (2024版).pdf",
        "new_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
        "name": "校园安全手册 (2024版)",
        "extension": ".pdf",
    }
    assert result == expected, "Test case 1 failed"
    
    # Test case 2: Merge with duplicate keys (should keep first occurrence)
    info1 = {"key": "value1"}
    info2 = {"key": "value2"}
    result = merge_file_info(info1, info2)
    assert result == {"key": "value1"}, "Test case 2 failed"
    
    # Test case 3: Special handling of created_time
    info1 = {"created_time": "2024-01-01"}
    info2 = {"created_time": "2024-01-01"}  # Same value
    result = merge_file_info(info1, info2)
    assert result == {"created_time": "2024-01-01"}, "Test case 3 failed"
    
    # Test case 4: Different created_time values (should keep first)
    info1 = {"created_time": "2024-01-01"}
    info2 = {"created_time": "2024-02-01"}  # Different value
    result = merge_file_info(info1, info2)
    assert result == {"created_time": "2024-01-01"}, "Test case 4 failed"
    
    # Test case 5: Empty dictionaries
    assert merge_file_info({}, {}) == {}, "Test case 5 failed"
    
    # Test case 6: Original example from the code
    info1 = {
        "file_name": "校园安全手册 (2024版).pdf",
        "new_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
        "old_path": "/downloads/校园安全手册 (2024版).pdf",
        "ai_description": "校园安全手册2024年更新版，涵盖消防、交通、心理健康等安全知识，指导学生处理突发事件。",
        "short_content": "2024校园安全手册"
    }
    
    info2 = {
        "name": "校园安全手册 (2024版)",
        "absolut_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
        "extension": ".pdf",
        "created_time": "2024-03-01 10:15:30",
        "size": "348672",
        "content": "校园安全手册2024年更新版，涵盖消防、交通、心理健康等安全知识，指导学生处理突发事件。"
    }
    
    result = merge_file_info(info1, info2)
    expected = {
        "file_name": "校园安全手册 (2024版).pdf",
        "new_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
        "old_path": "/downloads/校园安全手册 (2024版).pdf",
        "ai_description": "校园安全手册2024年更新版，涵盖消防、交通、心理健康等安全知识，指导学生处理突发事件。",
        "short_content": "2024校园安全手册",
        "name": "校园安全手册 (2024版)",
        "absolut_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
        "extension": ".pdf",
        "created_time": "2024-03-01 10:15:30",
        "size": "348672",
        "content": "校园安全手册2024年更新版，涵盖消防、交通、心理健康等安全知识，指导学生处理突发事件。"
    }
    assert result == expected, "Test case 6 failed"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_merge_file_info()
    print("\nOriginal example output:")
    # Run the original example and print the output
    info1 = {
        "file_name": "校园安全手册 (2024版).pdf",
        "new_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
        "old_path": "/downloads/校园安全手册 (2024版).pdf",
        "ai_description": "校园安全手册2024年更新版，涵盖消防、交通、心理健康等安全知识，指导学生处理突发事件。",
        "short_content": "2024校园安全手册"
    }
    
    info2 = {
        "name": "校园安全手册 (2024版)",
        "absolut_path": "/home/user/university_files/学生事务/校园安全手册 (2024版).pdf",
        "extension": ".pdf",
        "created_time": "2024-03-01 10:15:30",
        "size": "348672",
        "content": "校园安全手册2024年更新版，涵盖消防、交通、心理健康等安全知识，指导学生处理突发事件。"
    }
    
    result = merge_file_info(info1, info2)
    print(json.dumps(result, indent=2, ensure_ascii=False))