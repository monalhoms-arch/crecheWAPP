import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('CHARGILY_API_KEY')
secret_key = os.getenv('CHARGILY_SECRET_KEY')

def mask(s):
    if not s: return "MISSING"
    if s.startswith("your_"): return "PLACEHOLDER"
    return f"{s[:5]}...{s[-5:]}"

print(f"CHARGILY_API_KEY: {mask(api_key)}")
print(f"CHARGILY_SECRET_KEY: {mask(secret_key)}")
