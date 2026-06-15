import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
db = client["ecotracker_db"]
estoque_colecao = db["estoque"]

def inicializar_banco():
    """Verifica a conexão com o banco de dados"""
    try:
        client.admin.command('ping')
        print("Conexão com o MongoDB Atlas estabelecida com sucesso!")
    except Exception as e:
        print(f"X Erro critico ao conectar no MongoDB: {e}")

def salvar_produto(produto):
    """Insere um produto no banco de dados"""
    try:
        if estoque_colecao is not None:
            estoque_colecao.insert_one(produto)
            return True
        return False
    except Exception as e:
        print(f"Erro ao salvar produto: {e}")
        return False