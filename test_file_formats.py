import requests
import pandas as pd
import io
import zipfile
import os

BASE_URL = "http://localhost:8000"

def test_excel_file():
    """Test Excel file upload and cleaning"""
    print("\n=== Testing Excel File Support ===")
    
    # Create a test Excel file
    data = {
        "normal": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "high_null": [1, 2, None, None, None, None, None, None, 9, 10],  # 60% null
        "outliers": [1000, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    }
    df = pd.DataFrame(data)
    
    # Save to Excel
    excel_path = "test_excel.xlsx"
    df.to_excel(excel_path, index=False)
    
    # Upload and analyze
    print("1. Uploading Excel file...")
    with open(excel_path, 'rb') as f:
        files = {'file': ('test_data.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        res_analyze = requests.post(f"{BASE_URL}/analyze", files=files)
    
    if res_analyze.status_code != 200:
        print(f"   [FAIL] Analyze failed: {res_analyze.text}")
        os.remove(excel_path)
        return False
    
    data = res_analyze.json()
    file_id = data['file_id']
    print(f"   [OK] File ID: {file_id}")
    print(f"   [OK] Type: {data['type']}")
    print(f"   [OK] Original rows: {data['analysis']['rows']}")
    print(f"   [OK] Original columns: {data['analysis']['columns']}")
    
    # Clean
    print("2. Cleaning Excel file...")
    res_clean = requests.post(f"{BASE_URL}/clean/{file_id}")
    if res_clean.status_code != 200:
        print(f"   [FAIL] Clean failed: {res_clean.text}")
        os.remove(excel_path)
        return False
    
    result = res_clean.json()
    print(f"   [OK] Cleaned rows: {result['stats']['cleaned_rows']}")
    print(f"   [OK] Cleaned columns: {result['stats']['cleaned_columns']}")
    print(f"   [OK] Removed columns: {result['report']['removed_columns']}")
    
    # Cleanup
    os.remove(excel_path)
    return True

def test_zip_file():
    """Test ZIP file upload and cleaning"""
    print("\n=== Testing ZIP File Support ===")
    
    # Create a test CSV
    data = {
        "col1": [1, 2, 3, 4, 5],
        "col2": [10, 20, 30, 40, 50],
        "null_col": [None, None, None, None, None]  # 100% null
    }
    df = pd.DataFrame(data)
    csv_path = "test_data.csv"
    df.to_csv(csv_path, index=False)
    
    # Create ZIP file
    zip_path = "test_data.zip"
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(csv_path)
    
    # Upload and analyze
    print("1. Uploading ZIP file...")
    with open(zip_path, 'rb') as f:
        files = {'file': ('test_data.zip', f, 'application/zip')}
        res_analyze = requests.post(f"{BASE_URL}/analyze", files=files)
    
    if res_analyze.status_code != 200:
        print(f"   [FAIL] Analyze failed: {res_analyze.text}")
        os.remove(csv_path)
        os.remove(zip_path)
        return False
    
    data = res_analyze.json()
    file_id = data['file_id']
    print(f"   [OK] File ID: {file_id}")
    print(f"   [OK] Type: {data['type']}")
    print(f"   [OK] Extracted file: {data.get('extracted_file', 'N/A')}")
    print(f"   [OK] Original rows: {data['analysis']['rows']}")
    print(f"   [OK] Original columns: {data['analysis']['columns']}")
    
    # Clean
    print("2. Cleaning ZIP file...")
    res_clean = requests.post(f"{BASE_URL}/clean/{file_id}")
    if res_clean.status_code != 200:
        print(f"   [FAIL] Clean failed: {res_clean.text}")
        os.remove(csv_path)
        os.remove(zip_path)
        return False
    
    result = res_clean.json()
    print(f"   [OK] Cleaned rows: {result['stats']['cleaned_rows']}")
    print(f"   [OK] Cleaned columns: {result['stats']['cleaned_columns']}")
    print(f"   [OK] Removed columns: {result['report']['removed_columns']}")
    
    # Cleanup
    os.remove(csv_path)
    os.remove(zip_path)
    return True

if __name__ == "__main__":
    print("Starting File Format Tests...")
    
    excel_success = test_excel_file()
    zip_success = test_zip_file()
    
    print("\n=== Test Summary ===")
    print(f"Excel Support: {'[PASSED]' if excel_success else '[FAILED]'}")
    print(f"ZIP Support: {'[PASSED]' if zip_success else '[FAILED]'}")
    
    if excel_success and zip_success:
        print("\n[SUCCESS] All tests passed! Excel and ZIP support is working correctly.")
    else:
        print("\n[WARNING] Some tests failed. Please check the errors above.")
