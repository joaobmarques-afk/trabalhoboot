import json
import os

from api_produtos import buscar_produto_por_barcode, exibir_info_produto
from src.database import inicializar_banco, salvar_produto, listar_produtos

__version__ = "1.0.0"
ARQUIVO_DADOS = "estoque.json"


def carregar_dados():
    """Carrega dados do arquivo JSON."""
    if not os.path.exists(ARQUIVO_DADOS):
        return {}
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_dados(estoque):
    """Salva dados no arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(estoque, arquivo, indent=4, ensure_ascii=False)


def adicionar_produto(estoque, nome, quantidade):
    """Adiciona um produto ao estoque."""
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    nome_normalizado = nome.strip().lower()
    if nome_normalizado in estoque:
        estoque[nome_normalizado] += quantidade
    else:
        estoque[nome_normalizado] = quantidade
    return estoque


def remover_produto(estoque, nome, quantidade):
    """Remove um produto do estoque."""
    nome_normalizado = nome.strip().lower()
    if nome_normalizado not in estoque:
        raise KeyError("Erro: Produto não encontrado.")
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    if estoque[nome_normalizado] < quantidade:
        raise ValueError("Erro: Quantidade maior que o estoque.")
    estoque[nome_normalizado] -= quantidade
    if estoque[nome_normalizado] == 0:
        del estoque[nome_normalizado]
    return estoque


def buscar_produto_api(barcode):
    """Busca um produto na API Open Food Facts por código de barras e salva no banco."""
    try:
        info = buscar_produto_por_barcode(barcode)
        exibir_info_produto(info)
        
        # Se o produto for encontrado com sucesso, salvamos também no PostgreSQL em nuvem
        if info and info.get("encontrado"):
            salvar_produto(
                nome=info.get("nome", "Desconhecido"),
                codigo_barras=barcode,
                marca=info.get("marca", "Não informada"),
                categoria=info.get("categoria", "Não informada")
            )
            print("💾 Produto salvo com sucesso no Banco de Dados em Nuvem!")
            
        return info
    except ValueError as exc:
        print(f"Erro: {str(exc)}")
        return None
    except ConnectionError as exc:
        print(f"Erro de conexão: {str(exc)}")
        return None


def listar_estoque(estoque):
    """Lista todos os produtos do estoque."""
    if not estoque:
        print("\nESTOQUE VAZIO\n")
        return

    print("\n" + "=" * 60)
    print("LISTAGEM DO ESTOQUE")
    print("=" * 60)
    for nome, quantidade in estoque.items():
        print(f"   • {nome.upper()}: {quantidade} unidades")
    print("=" * 60 + "\n")


def menu_principal():
    """Menu interativo do sistema."""
    estoque = carregar_dados()

    while True:
        print("\n" + "=" * 60)
        print(
            "SISTEMA DE GERENCIAMENTO DE ESTOQUE "
            "- EcoTracker"
        )
        print("=" * 60)
        print("1. Adicionar produto (manual)")
        print("2. Adicionar produto (por código de barras/API)")
        print("3. Remover produto")
        print("4. Listar estoque")
        print("5. Buscar produto na API")
        print("6. Sair")
        print("=" * 60)

        opcao = input("Escolha uma opção (1-6): ").strip()

        if opcao == "1":
            nome = input("Nome do produto: ").strip()
            try:
                quantidade = int(input("Quantidade: "))
                estoque = adicionar_produto(estoque, nome, quantidade)
                salvar_dados(estoque)
                print(f"Produto '{nome}' adicionado com sucesso!")
            except ValueError as exc:
                print(f"Erro: {str(exc)}")

        elif opcao == "2":
            barcode = input(
                "Digite o código de barras (EAN): "
            ).strip()
            info = buscar_produto_api(barcode)
            if info and info["encontrado"]:
                try:
                    quantidade = int(
                        input("Quantidade a adicionar: ")
                    )
                    nome_produto = info["nome"].lower()
                    estoque = adicionar_produto(
                        estoque,
                        nome_produto,
                        quantidade,
                    )
                    salvar_dados(estoque)
                    print(
                        f"Produto '{info['nome']}' "
                        "adicionado com sucesso!"
                    )
                except ValueError as exc:
                    print(f"Erro: {str(exc)}")

        elif opcao == "3":
            nome = input(
                "Nome do produto a remover: "
            ).strip()
            try:
                quantidade = int(
                    input("Quantidade a remover: ")
                )
                estoque = remover_produto(
                    estoque,
                    nome,
                    quantidade,
                )
                salvar_dados(estoque)
                print(
                    f"Produto '{nome}' "
                    "removido com sucesso!"
                )
            except (ValueError, KeyError) as exc:
                print(f"Erro: {str(exc)}")

        elif opcao == "4":
            listar_estoque(estoque)

        elif opcao == "5":
            barcode = input(
                "Digite o código de barras para buscar (EAN): "
            ).strip()
            buscar_produto_api(barcode)

        elif opcao == "6":
            print("\nAté logo!\n")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    # Garante a criação da tabela no PostgreSQL na nuvem antes de rodar o menu interativo
    inicializar_banco()
    menu_principal()