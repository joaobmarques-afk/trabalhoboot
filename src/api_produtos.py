import requests


def buscar_produto_por_barcode(barcode):
    """
    Busca informações de produto na API Open Food Facts.

    Args:
        barcode (str): Código de barras do produto (EAN-13)

    Returns:
        dict: Dados do produto com as chaves:
            - nome: Nome do produto
            - marca: Marca do produto
            - categoria: Categoria principal
            - pais: País de origem
            - encontrado: True se produto existe, False caso contrário

    Raises:
        ValueError: Se o código de barras for inválido
        ConnectionError: Se houver erro de conexão com a API
    """
    barcode_limpo = ''.join(filter(str.isdigit, barcode))

    if len(barcode_limpo) not in [8, 12, 13]:
        raise ValueError(
            "Código de barras inválido. "
            "Use 8, 12 ou 13 dígitos."
        )

    base_url = "https://world.openfoodfacts.org/api/v0/product/"
    url = f"{base_url}{barcode_limpo}.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            return {
                "encontrado": False,
                "nome": None,
                "marca": None,
                "categoria": None,
                "pais": None,
            }

        product = data.get("product", {})

        return {
            "encontrado": True,
            "nome": product.get("product_name", "Nome não disponível"),
            "marca": product.get("brands", "Marca não disponível"),
            "categoria": product.get(
                "categories",
                "Categoria não disponível",
            ),
            "pais": product.get("countries", "País não disponível"),
        }

    except requests.exceptions.Timeout as exc:
        raise ConnectionError(
            "Timeout ao conectar com a API Open Food Facts"
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise ConnectionError(
            f"Erro ao conectar com a API: {str(exc)}"
        ) from exc


def exibir_info_produto(info):
    """
    Exibe as informações do produto de forma formatada.

    Args:
        info (dict): Retorno de buscar_produto_por_barcode
    """
    print("\n" + "=" * 50)
    if not info["encontrado"]:
        print("PRODUTO NÃO ENCONTRADO")
        print("=" * 50)
        return

    print("PRODUTO ENCONTRADO")
    print("=" * 50)
    print(f"Nome:      {info['nome']}")
    print(f"Marca:     {info['marca']}")
    print(f"Categoria: {info['categoria']}")
    print(f"País:      {info['pais']}")
    print("=" * 50 + "\n")
