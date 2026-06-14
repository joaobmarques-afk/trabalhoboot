import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Conexão com o MongoDB Atlas estabelecida com sucesso!")
    db = client["ecotracker_db"]
    estoque_colecao = db["estoque"]
except Exception as e:
    print("X Erro critico ao conectar no MongoDB: {e}")
    estoque_colecao = None
