import httpx
import asyncio
import os

BASE_URL = "http://localhost:8000"
TEST_FILE = "test_data.csv"

async def run_test():
    async with httpx.AsyncClient() as client:
        print(f"Testing against {BASE_URL}...")
        
        # 1. Analyze
        print(f"\n[1] Uploading & Analyzing {TEST_FILE}...")
        files = {'file': (TEST_FILE, open(TEST_FILE, 'rb'), 'text/csv')}
        try:
            r = await client.post(f"{BASE_URL}/analyze", files=files)
            r.raise_for_status()
            data = r.json()
            print("Response:", data)
            file_id = data.get("file_id")
            assert file_id, "File ID not returned"
            print("analysis['missing_values']:", data['analysis']['missing_values'])
            assert data['analysis']['missing_values']['age'] > 0, "Failed to detect missing values"
            print("[SUCCESS] Analysis Successful")
        except Exception as e:
            print(f"[FAILED] Analysis Failed: {e}")
            return

        # 2. Clean
        print(f"\n[2] Cleaning File ID: {file_id}...")
        try:
            r = await client.post(f"{BASE_URL}/clean/{file_id}")
            r.raise_for_status()
            result = r.json()
            print("Response:", result)
            assert result['status'] == 'success'
            download_url = result['download_url']
            print("[SUCCESS] Cleaning Triggered Successfully")
        except Exception as e:
            print(f"[FAILED] Cleaning Failed: {e}")
            return

        # 3. Download
        print(f"\n[3] Downloading Cleaned Data from {download_url}...")
        try:
            # Fix URL if relative
            if download_url.startswith("/"):
                url = f"{BASE_URL}{download_url}"
            else:
                url = download_url
                
            r = await client.get(url)
            r.raise_for_status()
            content = r.text
            print("Cleaned Content Preview:", content.splitlines()[:5])
            print("[SUCCESS] Download Successful")
        except Exception as e:
            print(f"[FAILED] Download Failed: {e}")
            return
            
        print("\n ALL BACKEND TESTS PASSED ")

if __name__ == "__main__":
    if not os.path.exists(TEST_FILE):
        print("Test file not found!")
    else:
        asyncio.run(run_test())
