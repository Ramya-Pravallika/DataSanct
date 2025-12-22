import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

def test_excel_quick():
    """Quick Excel file test"""
    print("Testing Excel file upload...")
    
    # Create test Excel file
    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    df = pd.DataFrame(data)
    df.to_excel("quick_test.xlsx", index=False)
    
    # Upload
    with open("quick_test.xlsx", 'rb') as f:
        files = {'file': ('quick_test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        res = requests.post(f"{BASE_URL}/analyze", files=files)
    
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        print("[OK] Excel upload successful!")
        print(f"Response: {res.json()}")
    else:
        print(f"[FAIL] Error: {res.text}")
    
    import os
    os.remove("quick_test.xlsx")

if __name__ == "__main__":
    test_excel_quick()
