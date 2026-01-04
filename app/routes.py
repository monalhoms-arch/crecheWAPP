from app import app, db
from flask import jsonify

@app.route("/")
def index():
    return jsonify({"message": "Flask + MongoDB Docker is running!"})
