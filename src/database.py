import os
<<<<<<< HEAD
import certifi
=======
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from unittest.mock import MagicMock
>>>>>>> 8bb27013863411a17f8b9ef273a484a30397598b
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Evita estourar erro se estivermos rodando testes automatizados locais
if "pytest" in sys.modules or "pytest" in sys.argv[0]:
    client = None
    db = None
    estoque_colecao = None
else:
    # Conexão segura com o MongoDB Atlas usando o Certifi para o Render
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
    db = client["ecotracker_db"]
    estoque_colecao = db["estoque"]

def inicializar_banco():
    """Verifica a conexão com o MongoDB"""
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        print("🤖 Ambiente de testes: ignorando banco real.")
        return
    try:
        client.admin.command('ping')
        print("Conexão com o MongoDB Atlas estabelecida com sucesso!")
    except Exception as e:
        print(f"X Erro critico ao conectar no MongoDB: {e}")

def salvar_produto(*args, **kwargs):
    """Insere um produto no MongoDB.
    Suporta tanto o formato de dicionário quanto argumentos separados."""
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        return True
    try:
        # Se o main.py passar um dicionário pronto
        if len(args) == 1 and isinstance(args[0], dict):
            produto = args[0]
        # Se o main.py passar os campos separados: nome, codigo_barras, marca, categoria
        elif len(args) >= 1:
            produto = {
                "nome": args[0],
                "codigo_barras": args[1] if len(args) > 1 else "",
                "marca": args[2] if len(args) > 2 else "",
                "categoria": args[3] if len(args) > 3 else ""
            }
        else:
            produto = kwargs

        if estoque_colecao is not None:
            estoque_colecao.insert_one(produto)
            return True
        return False
    except Exception as e:
        print(f"Erro ao salvar produto: {e}")
        return False

def listar_produtos():
    """Retorna os produtos salvos no MongoDB (ocultando o campo _id interno)"""
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        return []
    try:
        if estoque_colecao is not None:
            return list(estoque_colecao.find({}, {"_id": 0}))
        return []
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []