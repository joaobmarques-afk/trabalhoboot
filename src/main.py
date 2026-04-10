import json
import os

__version__ = "1.0.0"
ARQUIVO_DADOS = "estoque.json"


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {}
    with open(ARQUIVO_DADOS, 'r') as f:
        return json.load(f)


def salvar_dados(estoque):
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump(estoque, f, indent=4)


def adicionar_produto(estoque, nome, quantidade):
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    nome = nome.strip().lower()
    if nome in estoque:
        estoque[nome] += quantidade
    else:
        estoque[nome] = quantidade
    return estoque


def remover_produto(estoque, nome, quantidade):
    nome = nome.strip().lower()
    if nome not in estoque:
        raise KeyError("Erro: Produto não encontrado.")
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    if estoque[nome] < quantidade:
        raise ValueError("Erro: Quantidade maior que o estoque.")
    estoque[nome] -= quantidade
    if estoque[nome] == 0:
        del estoque[nome]
    return estoque