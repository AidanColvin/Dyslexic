import requests
import os
import sys

# Simple test suite to verify if your Private/Public switch actually works
BASE_URL = "http://localhost:5000"

def test_public_access():
    print("Testing Public Access...")
    try:
        r = requests.get(f"{BASE_URL}/status")
        if r.status_code == 200:
            print("✅ Status Endpoint is OPEN (Correct)")
        else:
            print(f"❌ Status failed: {r.status_code}")
            
        # Try a sensitive endpoint without auth
        r = requests.post(f"{BASE_URL}/dyslexia/v2/suggest", json={})
        if r.status_code == 200:
            print("⚠️ Suggest Endpoint is PUBLIC (Check if this was intended)")
        elif r.status_code == 401:
            print("🔒 Suggest Endpoint is SECURED (Correct for Private Mode)")
    except Exception as e:
        print(f"❌ Server not reachable: {e}")

if __name__ == "__main__":
    test_public_access()
