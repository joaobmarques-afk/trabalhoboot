import requests

from src.api_produtos import buscar_produto_por_barcode


class FakeResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"Status code: {self.status_code}"
            )

    def json(self):
        return self._json_data


def test_buscar_produto_por_barcode_sucesso(monkeypatch):
    """Deve retornar dados quando a API responde com produto encontrado."""

    def fake_get(url, timeout=10):
        data = {
            "status": 1,
            "product": {
                "product_name": "Produto Teste",
                "brands": "Marca Teste",
                "categories": "Categoria Teste",
                "countries": "Brasil",
            },
        }
        return FakeResponse(status_code=200, json_data=data)

    monkeypatch.setattr(requests, "get", fake_get)

    resultado = buscar_produto_por_barcode("12345678")

    assert resultado["encontrado"] is True
    assert resultado["nome"] == "Produto Teste"
    assert resultado["marca"] == "Marca Teste"
    assert resultado["categoria"] == "Categoria Teste"
    assert resultado["pais"] == "Brasil"


def test_buscar_produto_por_barcode_nao_encontrado(monkeypatch):
    """Deve marcar como não encontrado quando status != 1."""

    def fake_get(url, timeout=10):
        data = {
            "status": 0,
        }
        return FakeResponse(status_code=200, json_data=data)

    monkeypatch.setattr(requests, "get", fake_get)

    resultado = buscar_produto_por_barcode("99999999")

    assert resultado["encontrado"] is False
    assert resultado["nome"] is None
    assert resultado["marca"] is None
    assert resultado["categoria"] is None
    assert resultado["pais"] is None


def test_buscar_produto_por_barcode_timeout(monkeypatch):
    """Deve lançar ConnectionError em caso de timeout."""

    def fake_get(url, timeout=10):
        raise requests.exceptions.Timeout("timeout")

    monkeypatch.setattr(requests, "get", fake_get)

    try:
        buscar_produto_por_barcode("12345678")
        assert False, "Era esperado ConnectionError"
    except ConnectionError:
        assert True
