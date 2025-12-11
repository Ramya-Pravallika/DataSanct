import requests
import pandas as pd
import io
import time

BASE_URL = "http://localhost:8000"

def create_test_csv():
    # Create a CSV with 1 normal col, 1 high-null col (60% nulls), 1 outlier col
    data = {
        "normal": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "high_null": [1, 2, None, None, None, None, None, None, 9, 10], # 60% null
        "outliers": [1000, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    }
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def test_flow():
    print("1. Creating Test CSV...")
    csv_content = create_test_csv()
    
    print("2. Uploading & Analyzing...")
    files = {'file': ('test_auto.csv', csv_content, 'text/csv')}
    res_analyze = requests.post(f"{BASE_URL}/analyze", files=files)
    
    if res_analyze.status_code != 200:
        print(f"Analyze failed: {res_analyze.text}")
        return
        
    data = res_analyze.json()
    file_id = data['file_id']
    print(f"   File ID: {file_id}")
    print(f"   Plan: {data['plan']['plan']}")
    
    # Check if plan contains drop_columns for 'high_null'
    plan_steps = data['plan']['plan']
    has_drop = any(s['action'] == 'drop_columns' and 'high_null' in s['columns'] for s in plan_steps)
    print(f"   [Verify] Plan suggests dropping 'high_null': {has_drop}")
    
    print("3. Cleaning...")
    res_clean = requests.post(f"{BASE_URL}/clean/{file_id}")
    if res_clean.status_code != 200:
        print(f"Clean failed: {res_clean.text}")
        return
        
    result = res_clean.json()
    print("   Clean Response Stats:", result['stats'])
    print("   Clean Response Report:", result['report'])
    
    # Assertions
    if "high_null" in result['report']['removed_columns']:
        print("   [SUCCESS] 'high_null' column was correctly removed.")
    else:
        print("   [FAILURE] 'high_null' column was NOT removed.")
        
    if result['report']['outliers_removed'] > 0:
        print("   [SUCCESS] Outliers were removed.")
    else:
        print("   [FAILURE] No outliers removed.")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Test Execution Failed: {e}")
