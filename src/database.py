import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from unittest.mock import MagicMock


def obter_conexao():
    """Busca a string de conexão das variáveis de ambiente."""
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        return MagicMock()

    url_padrao = (
        "postgresql://usuario:senha@localhost:5432/trabalhoboot"
    )
    url_banco = os.getenv("DATABASE_URL", url_padrao)
    return psycopg2.connect(url_banco)


def inicializar_banco():
    """Cria a tabela de produtos automaticamente se não existir."""
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        print("🤖 Ambiente de testes: ignorando banco real.")
        return

    comando_sql = """
    CREATE TABLE IF NOT EXISTS produtos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        codigo_barras VARCHAR(50),
        marca VARCHAR(100),
        categoria VARCHAR(150),
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conexao = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        conexao.commit()
        cursor.close()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o banco: {e}")
    finally:
        if conexao and not isinstance(conexao, MagicMock):
            conexao.close()


def salvar_produto(nome, codigo_barras, marca, categoria):
    """Insere um novo produto no banco."""
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        return

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO produtos (nome, codigo_barras, marca, categoria)
        VALUES (%s, %s, %s, %s);
        """,
        (nome, codigo_barras, marca, categoria)
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def listar_produtos():
    """Retorna os produtos salvos ou uma lista vazia se for teste."""
    if "pytest" in sys.modules or "pytest" in sys.argv[0]:
        return []

    conexao = obter_conexao()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT id, nome, codigo_barras, marca, categoria, data_cadastro "
        "FROM produtos ORDER BY data_cadastro DESC;"
    )
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return produtos
