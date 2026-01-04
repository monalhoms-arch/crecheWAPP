from pymongo import MongoClient
import os

# استخدام المتغير البيئي من docker-compose
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/creche_db")

client = MongoClient(MONGO_URI)
db = client['creche_db']

# مثال على مجموعة
children_collection = db['children']
