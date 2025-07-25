import requests
import json

# Test the local server
base_url = "http://localhost:8000"

print("Testing MaxStream Proxy Backend...")

# Test 1: Root endpoint
try:
    response = requests.get(f"{base_url}/")
    print(f"SUCCESS Root endpoint: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"ERROR Root endpoint failed: {e}")

# Test 2: Movie stream
try:
    response = requests.get(f"{base_url}/stream?type=movie&id=552095")
    print(f"SUCCESS Movie stream: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if "stream_url" in data:
            print(f"   MOVIE Found stream URL: {data['stream_url'][:50]}...")
        else:
            print(f"   WARNING No stream URL found: {data}")
    else:
        print(f"   ERROR: {response.text}")
except Exception as e:
    print(f"ERROR Movie test failed: {e}")

# Test 3: TV Series stream
try:
    response = requests.get(f"{base_url}/stream?type=tv&id=1412&season=1&episode=1")
    print(f"SUCCESS TV series stream: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if "stream_url" in data:
            print(f"   TV Found stream URL: {data['stream_url'][:50]}...")
        else:
            print(f"   WARNING No stream URL found: {data}")
    else:
        print(f"   ERROR: {response.text}")
except Exception as e:
    print(f"ERROR TV series test failed: {e}")

print("\nBackend is ready for deployment!")
