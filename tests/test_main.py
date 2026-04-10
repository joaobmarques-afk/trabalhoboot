import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from main import adicionar_produto, remover_produto

def test_adicionar_produto_corretamente():
    estoque = adicionar_produto({}, "Caneta", 50)
    assert estoque["caneta"] == 50

def test_impedir_quantidade_negativa():
    with pytest.raises(ValueError):
        adicionar_produto({"caderno": 10}, "caderno", -5)

def test_remover_mais_que_o_estoque():
    with pytest.raises(ValueError):
        remover_produto({"borracha": 5}, "borracha", 10)