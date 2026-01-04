import requests
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv('CHARGILY_SECRET_KEY')

urls = [
    'https://pay.chargily.com/test/api/v2/checkouts',
    'https://pay.chargily.com/api/v2/checkouts',
    'https://pay.chargily.net/test/api/v2/checkouts',
    'https://pay.chargily.net/api/v2/checkouts'
]

payload = {
    "amount": 1000,
    "currency": "dzd",
    "success_url": "https://example.com/success"
}

headers = {
    'Authorization': f'Bearer {secret_key}',
    'Content-Type': 'application/json'
}

for url in urls:
    print(f"Testing URL: {url}")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201 or response.status_code == 200:
            print(f"SUCCESS on URL: {url}")
            # break  # Remove break to test all urls
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
