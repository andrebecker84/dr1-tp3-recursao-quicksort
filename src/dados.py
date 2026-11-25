"""Entradas dos experimentos. A semente é fixa: toda execução gera os mesmos dados."""
import os
import random
from enum import StrEnum

SEMENTE = 42
ARRAY_DO_LIVRO = (0, 5, 2, 1, 6, 3)         # exemplo de partição de Wengrow (2023, cap. 13)
PESOS_DO_LIVRO = (11, 8, 7, 6, 5)           # mochila clássica: alvo 20, solução 8 + 7 + 5
ALVO_DO_LIVRO = 20
FRACAO_FORA_DO_LUGAR = 20                   # quase ordenada: 1 troca de vizinhos a cada 20 elementos

# Árvore de exemplo do Exercício 4: diretório -> dicionário; arquivo -> None.
ARVORE_EXEMPLO = {
    "README.md": None,
    ".gitignore": None,
    "dados": {
        "entradas.csv": None,
        "brutos": {"2025": {"jan.csv": None, "fev.csv": None}, "2026": {"jan.csv": None}},
    },
    "docs": {"relatorio.md": None, "imagens": {"grafico.png": None, "tela.png": None}},
    "src": {"main.py": None, "util": {"__init__.py": None, "texto.py": None}},
    "vazio": {},
}


class Cenario(StrEnum):
    ORDENADA = "ordenada"
    INVERTIDA = "invertida"
    ALEATORIA = "aleatória"
    QUASE_ORDENADA = "quase ordenada"
    REPETIDOS = "muitos repetidos"


def lista_no_cenario(n, cenario, semente=SEMENTE):
    """N inteiros na ordem do cenário: de 1 a N, ou de 1 a 10 no cenário com muitos repetidos."""
    gerador = random.Random(semente)
    if cenario is Cenario.REPETIDOS:
        return [gerador.randint(1, 10) for _ in range(n)]
    lista = list(range(1, n + 1))
    if cenario is Cenario.INVERTIDA:
        lista.reverse()
    elif cenario is Cenario.ALEATORIA:
        gerador.shuffle(lista)
    elif cenario is Cenario.QUASE_ORDENADA:
        for _ in range(max(1, n // FRACAO_FORA_DO_LUGAR)):
            i = gerador.randrange(n - 1)
            lista[i], lista[i + 1] = lista[i + 1], lista[i]
    return lista


def aleatorios(n, semente=SEMENTE):
    """N inteiros distintos embaralhados, entre 1 e 10·N."""
    return random.Random(semente).sample(range(1, 10 * n + 1), n)


def pesos_sequenciais(n):
    """Pesos 1, 2, ..., n e o alvo na metade da soma: o caso com mais soluções e mais redundância."""
    pesos = list(range(1, n + 1))
    return sum(pesos) // 2, pesos


def criar_arvore(destino, arvore=ARVORE_EXEMPLO):
    """Cria em disco a árvore de exemplo (recursivamente, como ela é percorrida depois)."""
    os.makedirs(destino, exist_ok=True)
    for nome, conteudo in arvore.items():
        caminho = os.path.join(destino, nome)
        if conteudo is None:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(f"{nome}\n")
        else:
            criar_arvore(caminho, conteudo)
