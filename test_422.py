import requests
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv('CHARGILY_SECRET_KEY')
url = 'https://pay.chargily.net/test/api/v2/checkouts'

headers = {
    'Authorization': f'Bearer {secret_key}',
    'Content-Type': 'application/json'
}

def test_payload(name, payload):
    print(f"Testing {name}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 30)

# Case 1: Amount < 100
test_payload("Small Amount (50)", {
    "amount": 50,
    "currency": "dzd",
    "success_url": "https://example.com/success"
})

# Case 2: Standard valid
test_payload("Standard Valid (150)", {
    "amount": 150,
    "currency": "dzd",
    "success_url": "https://example.com/success"
})

# Case 3: Metadata with non-string values
test_payload("Metadata with List", {
    "amount": 200,
    "currency": "dzd",
    "success_url": "https://example.com/success",
    "metadata": {"info": [1, 2, 3]}
})

# Case 4: Long description
test_payload("Long Description", {
    "amount": 200,
    "currency": "dzd",
    "success_url": "https://example.com/success",
    "description": "A" * 300
})
