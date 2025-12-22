import requests
import pandas as pd
import os

BASE_URL = "http://localhost:8000"

def test_full_excel_workflow():
    """Test complete Excel workflow: upload, analyze, clean"""
    print("=== Full Excel Workflow Test ===\n")
    
    # Create test Excel file
    data = {
        "normal": [1, 2, 3, 4, 5],
        "high_null": [1, None, None, None, 5],  # 60% null
        "values": [10, 20, 30, 40, 50]
    }
    df = pd.DataFrame(data)
    df.to_excel("test_workflow.xlsx", index=False)
    print("1. Created test Excel file")
    
    # Upload and analyze
    print("2. Uploading Excel file...")
    with open("test_workflow.xlsx", 'rb') as f:
        files = {'file': ('test_workflow.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        res_analyze = requests.post(f"{BASE_URL}/analyze", files=files)
    
    if res_analyze.status_code != 200:
        print(f"   [FAIL] Analyze failed: {res_analyze.text}")
        os.remove("test_workflow.xlsx")
        return False
    
    data = res_analyze.json()
    file_id = data['file_id']
    print(f"   [OK] File analyzed - ID: {file_id}")
    print(f"   [OK] Original rows: {data['analysis']['rows']}, columns: {data['analysis']['columns']}")
    
    # Clean
    print("3. Cleaning Excel file...")
    res_clean = requests.post(f"{BASE_URL}/clean/{file_id}")
    
    if res_clean.status_code != 200:
        print(f"   [FAIL] Clean failed!")
        print(f"   Status code: {res_clean.status_code}")
        print(f"   Error: {res_clean.text}")
        os.remove("test_workflow.xlsx")
        return False
    
    result = res_clean.json()
    print(f"   [OK] Cleaning successful!")
    print(f"   Stats: {result.get('stats', 'N/A')}")
    print(f"   Report: {result.get('report', 'N/A')}")
    print(f"   Download URL: {result.get('download_url', 'N/A')}")
    
    # Cleanup
    os.remove("test_workflow.xlsx")
    print("\n[SUCCESS] Full Excel workflow completed!")
    return True

if __name__ == "__main__":
    success = test_full_excel_workflow()
    exit(0 if success else 1)
