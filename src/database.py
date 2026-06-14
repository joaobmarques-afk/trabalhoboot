import os
import psycopg2
from psycopg2.extras import RealDictCursor

def obter_conexao():
    """
    Busca a string de conexão das variáveis de ambiente.
    Isso é um requisito do Barema para segurança no Streamlit Cloud.
    """
    # Se estiver rodando local sem a variável configurada, usamos um fallback temporário para teste
    url_banco = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/trabalhoboot")
    
    return psycopg2.connect(url_banco)

def inicializar_banco():
    """
    Cria a tabela de produtos automaticamente se ela não existir.
    Garante que o deploy funcione de primeira.
    """
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
        if conexao:
            conexao.close()

def salvar_produto(nome, codigo_barras, marca, categoria):
    """Insere um novo produto mapeado da API do Open Food Facts no banco."""
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
    """Retorna todos os produtos salvos para exibir no histórico do Streamlit."""
    conexao = obter_conexao()
    # RealDictCursor faz os dados virem em formato de dicionário, ideal para o Streamlit Dataframe
    cursor = conexao.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, nome, codigo_barras, marca, categoria, data_cadastro FROM produtos ORDER BY data_cadastro DESC;")
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return produtos