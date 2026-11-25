"""Exercício 6: problema da mochila por recursão pura, com todas as combinações que somam o alvo."""
import random

from algoritmos.metricas import medir
from algoritmos.mochila import knapsack
from apresentacao.terminal import compacta, milhar, ok, tabela, titulo
from dados import ALVO_DO_LIVRO, PESOS_DO_LIVRO, SEMENTE, pesos_sequenciais
from verificacao import subconjuntos_que_somam

CONJUNTOS = (
    (ALVO_DO_LIVRO, list(PESOS_DO_LIVRO)),
    (10, [2, 3, 5, 7, 8]),
    (12, [1, 2, 3, 4, 5, 6]),
    (10, [5, 5, 10]),
    (7, [2, 4, 6]),
    (0, [3, 4]),
    (100, list(range(1, 11))),
)
TAMANHOS = (4, 8, 12, 16, 20)
LARGURA = 60


def resumir(combinacoes):
    texto = " ".join(compacta(c) for c in combinacoes) or "nenhuma"
    return texto if len(texto) <= LARGURA else texto[:LARGURA - 4] + " ..."


def mostrar_conjuntos():
    titulo("Exercício 6: knapsack(target, weights, 0), combinações que somam exatamente o alvo")
    linhas = []
    for alvo, pesos in CONJUNTOS:
        combinacoes, metricas = medir(knapsack, alvo, pesos, 0)
        linhas.append([alvo, compacta(pesos), len(combinacoes), milhar(metricas.chamadas), resumir(combinacoes)])
    tabela(["alvo", "pesos", "soluções", "chamadas", "combinações"], linhas, ">>>><")
    print("alvo 0 já é uma solução: a mochila vazia ([]); alvo ímpar com pesos pares ou acima da soma: nenhuma")


def mostrar_explosao():
    titulo("Explosão combinatória: pesos 1, 2, ..., n")
    linhas, exato = [], True
    for n in TAMANHOS:
        alvo, pesos = pesos_sequenciais(n)
        _, inatingivel = medir(knapsack, sum(pesos) + 1, pesos)
        solucoes, metade = medir(knapsack, alvo, pesos)
        exato = exato and inatingivel.chamadas == 2 ** (n + 1) - 1
        linhas.append([n, milhar(inatingivel.chamadas), milhar(2 ** (n + 1) - 1), alvo, milhar(metade.chamadas),
                       milhar(len(solucoes))])
    tabela(["n", "chamadas (alvo inatingível)", "2^(n+1) − 1", "alvo = soma/2", "chamadas", "soluções"], linhas,
           ">>>>>>")
    ok(exato, "sem nenhum corte, cada peso dobra a árvore: 2^(n+1) − 1 chamadas, O(2^n)")
    print("cada peso a mais multiplica as chamadas por 2: com n = 40 seriam 2,2 trilhões")


def mostrar_verificacoes():
    titulo("Verificações")
    gerador = random.Random(SEMENTE)
    casos = []
    for _ in range(200):
        pesos = [gerador.randint(1, 15) for _ in range(gerador.randint(0, 12))]
        casos.append((gerador.randint(0, 40), pesos))
    ok(all(sorted(sorted(c) for c in knapsack(a, p)) == subconjuntos_que_somam(a, p) for a, p in casos),
       f"as mesmas soluções da enumeração das 2^n máscaras de bits em {len(casos)} conjuntos aleatórios")
    ok(all(sum(c) == a for a, p in casos for c in knapsack(a, p)), "toda combinação devolvida soma exatamente o alvo")
    try:
        knapsack(5, [2, 0, 3])
        recusou = False
    except ValueError:
        recusou = True
    ok(recusou, "peso zero ou negativo é recusado: o corte em alvo < 0 só é seguro com pesos positivos")


def main():
    mostrar_conjuntos()
    print()
    mostrar_explosao()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
