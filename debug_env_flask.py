from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/debug-env')
def debug_env():
    sk = os.getenv('CHARGILY_SECRET_KEY')
    pk = os.getenv('CHARGILY_API_KEY')
    
    def mask(s):
        if not s: return "None"
        return f"{s[:7]}...{s[-4:]}"
    
    return {
        "CHARGILY_SECRET_KEY": mask(sk),
        "CHARGILY_API_KEY": mask(pk),
        "SK_LENGTH": len(sk) if sk else 0
    }

if __name__ == "__main__":
    # Test directly
    sk = os.getenv('CHARGILY_SECRET_KEY')
    print(f"Direct check - SK: {sk[:7]}...{sk[-4:] if sk else ''}")
    print(f"Direct check - PK: {os.getenv('CHARGILY_API_KEY')[:7]}...")
