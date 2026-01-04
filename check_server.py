import requests

try:
    response = requests.get('http://localhost:5000')
    print(f"Server Status: {response.status_code}")
    print(f"Server is running: {'Yes' if response.status_code == 200 else 'No'}")
except Exception as e:
    print(f"Server Error: {e}")
    print("Server is NOT running")
