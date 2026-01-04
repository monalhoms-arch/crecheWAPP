from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

# إعداد MongoDB
mongo_client = MongoClient("mongodb://creche_mongo:27017/")
db = mongo_client['creche_db']

from app import routes
