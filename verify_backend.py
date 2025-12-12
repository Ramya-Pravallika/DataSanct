import requests
import time
import os

BASE_URL = "http://localhost:8000"
TEST_FILE = "server/messy_data.csv"

def test_cleaning_flow():
    print(f"Testing cleaning flow with {TEST_FILE}...")
    
    # 1. Upload & Analyze
    with open(TEST_FILE, 'rb') as f:
        files = {'file': (os.path.basename(TEST_FILE), f, 'text/csv')}
        response = requests.post(f"{BASE_URL}/analyze", files=files)
    
    if response.status_code != 200:
        print("Analysis failed:", response.text)
        return
        
    data = response.json()
    file_id = data['file_id']
    print(f"Analysis complete. File ID: {file_id}")
    print("DEBUG: Analysis Data:", data.get('analysis'))
    
    # Verify clean_text step is in plan
    plan_steps = [s['step'] for s in data['plan']['plan']]
    if 'clean_text' in plan_steps:
        print("SUCCESS: 'clean_text' step found in generated plan.")
    else:
        print("FAILURE: 'clean_text' step MISSING from plan.")
        print("Plan:", data['plan'])

    # 2. Clean
    print(f"Requesting cleaning for {file_id}...")
    clean_res = requests.post(f"{BASE_URL}/clean/{file_id}")
    
    if clean_res.status_code != 200:
        print("Cleaning failed:", clean_res.text)
        return
        
    clean_data = clean_res.json()
    print("Cleaning complete. Report:", clean_data.get('report'))
    
    # 3. Download and Verify Content
    download_url = clean_data['download_url'] # e.g. /download/cleaned_messy_data.csv
    print(f"Downloading result from {download_url}...")
    
    file_content = requests.get(f"{BASE_URL}{download_url}").text
    print("\n--- Cleaned File Content ---")
    print(file_content)
    print("----------------------------")
    
    # Simple check: "  Alice  " should become "Alice"
    if "Alice" in file_content and "  Alice  " not in file_content:
        print("SUCCESS: Whitespace stripped correctly.")
    else:
        print("FAILURE: Whitespace might still be present.")

    print("\n--- DEBUG INFO ---")
    print("Categorical Columns found:", data.get('analysis', {}).get('categorical_columns'))
    print("Full Analysis Keys:", list(data.get('analysis', {}).keys()))
    print("--------------------")

if __name__ == "__main__":
    # Ensure server is running before running this
    try:
        test_cleaning_flow()
    except Exception as e:
        print(f"Test failed with error: {e}")
        print("Make sure the backend server is running on port 8000")
