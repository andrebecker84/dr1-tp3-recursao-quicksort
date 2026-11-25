"""Exercício 7: chamadas redundantes e crescimento das chamadas, com foco no knapsack do Exercício 6."""
import os
import tempfile
from collections import Counter

from algoritmos.aritmetica import mult, power
from algoritmos.combinacoes import teams
from algoritmos.diretorios import percorrer
from algoritmos.fatoracao import factor
from algoritmos.metricas import medir
from algoritmos.mochila import knapsack
from apresentacao.terminal import decimal, milhar, ok, tabela, titulo
from dados import criar_arvore, pesos_sequenciais

EXEMPLO = (6, [1, 2, 3, 4])
TAMANHOS = (8, 12, 16, 20)


def visitas(alvo, pesos):
    """Quantas vezes cada estado (alvo restante, índice) foi visitado numa execução do knapsack."""
    contagem = Counter()

    def registrar(alvo_restante, indice, _nivel):
        contagem[(alvo_restante, indice)] += 1

    knapsack(alvo, pesos, ao_visitar=registrar)
    return contagem


def mostrar_exemplo():
    alvo, pesos = EXEMPLO
    titulo(f"Exercício 7: estados repetidos em knapsack({alvo}, {pesos})")
    contagem = visitas(alvo, pesos)
    linhas = [[f"({a}, {i})", vezes, "alvo já ultrapassado" if a < 0 else f"falta {a} com os pesos {pesos[i:]}"]
              for (a, i), vezes in contagem.items() if vezes > 1]
    tabela(["estado (alvo, índice)", "visitas", "subproblema"], linhas, "<><")
    print(f"{sum(contagem.values())} chamadas para {len(contagem)} estados distintos. O estado (3, 3) chega por dois "
          f"caminhos: pegar 1 e 2, ou pegar só o 3")


def mostrar_redundancia():
    titulo("Em escala: pesos 1, 2, ..., n e alvo = soma/2")
    linhas = []
    for n in TAMANHOS:
        alvo, pesos = pesos_sequenciais(n)
        contagem = visitas(alvo, pesos)
        chamadas, distintos = sum(contagem.values()), len(contagem)
        (estado, vezes), = contagem.most_common(1)
        linhas.append([n, milhar(chamadas), milhar(distintos), milhar(chamadas - distintos),
                       f"{decimal(100 * (chamadas - distintos) / chamadas)}%", f"{estado} × {milhar(vezes)}"])
    tabela(["n", "chamadas", "estados distintos", "redundantes", "% redundante", "estado mais repetido"], linhas,
           ">>>>>>")
    print("a cada 4 pesos, as chamadas crescem ≈ ×16 (2^4) e os estados distintos menos de ×3: o resto é trabalho repetido")


def chamadas(funcao, *args):
    return medir(funcao, *args)[1].chamadas


def tamanho_de_arvore(subdiretorios):
    """Chamadas do percorrer numa árvore com uma raiz e o número dado de subdiretórios lado a lado."""
    with tempfile.TemporaryDirectory() as raiz:
        criar_arvore(raiz, {f"d{i}": {"a.txt": None} for i in range(subdiretorios)})
        return chamadas(percorrer, raiz)


def mostrar_crescimento():
    titulo("Crescimento das chamadas ao dobrar a entrada, nas funções dos Exercícios 1 a 6")
    _, pesos_10 = pesos_sequenciais(10)
    _, pesos_20 = pesos_sequenciais(20)
    casos = [
        ("mult(5, y)", "y", 250, 500, chamadas(mult, 5, 250), chamadas(mult, 5, 500), "T(y) = T(y−1) + 1", "O(y)"),
        ("power(2, y)", "y", 500, 1_000, chamadas(power, 2, 500), chamadas(power, 2, 1_000), "T(y) = T(y/2) + 1", "O(log y)"),
        ("factor(2^k)", "k", 10, 20, chamadas(factor, 2 ** 10), chamadas(factor, 2 ** 20), "1 por fator", "O(log x)"),
        ("percorrer", "pastas", 10, 20, tamanho_de_arvore(10), tamanho_de_arvore(20), "1 por diretório", "O(D)"),
        ("teams(n, n/2)", "n", 8, 16, chamadas(teams, "ABCDEFGH", 4), chamadas(teams, "ABCDEFGHIJKLMNOP", 8),
         "T(n−1, k−1) + T(n−1, k)", "O(2^n)"),
        ("knapsack", "n", 10, 20, chamadas(knapsack, 56, pesos_10), chamadas(knapsack, 211, pesos_20),
         "T(n) = 2T(n−1) + 1", "O(2^n)"),
    ]
    linhas = [[nome, f"{variavel} = {a} → {b}", milhar(ca), milhar(cb), f"×{decimal(cb / ca)}",
               recorrencia, big_o] for nome, variavel, a, b, ca, cb, recorrencia, big_o in casos]
    tabela(["função", "entrada dobrada", "chamadas", "chamadas", "fator", "recorrência", "Big O (chamadas)"], linhas,
           "<<>>><<")
    return casos


def mostrar_verificacoes(casos):
    titulo("Verificações")
    alvo, pesos = pesos_sequenciais(20)
    contagem = visitas(alvo, pesos)
    ok(len(contagem) <= (len(pesos) + 1) * (2 * alvo + 1),
       f"estados distintos ({milhar(len(contagem))}) limitados por (n + 1)·(2·alvo + 1): crescem como n · alvo")
    lineares = [c for c in casos if c[-1] in ("O(y)", "O(D)")]
    ok(all(abs(cb / ca - 2) < 0.1 for *_, ca, cb, _, _ in lineares), "as recursões lineares dobram junto com a entrada")
    ok(casos[-1][5] == 2 ** 21 - 1 and casos[-1][4] == 2 ** 11 - 1,
       "o knapsack sem solução vai de 2^11 − 1 para 2^21 − 1 chamadas: ×1.024 ao dobrar n")


def main():
    mostrar_exemplo()
    print()
    mostrar_redundancia()
    print()
    casos = mostrar_crescimento()
    print()
    mostrar_verificacoes(casos)


if __name__ == "__main__":
    main()
