"""Exercício 8: o knapsack do Exercício 6 com memoização, comparando o número de chamadas."""
import random
import time

from algoritmos.metricas import medir
from algoritmos.mochila import contar_combinacoes, knapsack, knapsack_memo
from apresentacao.terminal import decimal, milhar, ok, tabela, titulo
from dados import SEMENTE, pesos_sequenciais

TAMANHOS = (8, 12, 16, 20)
TAMANHOS_SO_MEMO = (40, 60, 100)


def cronometrar(funcao, *args):
    inicio = time.perf_counter()
    resultado, metricas = medir(funcao, *args)
    return resultado, metricas, time.perf_counter() - inicio


def ordenadas(combinacoes):
    return sorted(sorted(c) for c in combinacoes)


def mostrar_comparacao():
    titulo("Exercício 8: knapsack puro x knapsack_memo, pesos 1, 2, ..., n e alvo = soma/2")
    linhas, iguais = [], True
    for n in TAMANHOS:
        alvo, pesos = pesos_sequenciais(n)
        pura, m_pura, t_pura = cronometrar(knapsack, alvo, pesos)
        memo, m_memo, t_memo = cronometrar(knapsack_memo, alvo, pesos)
        iguais = iguais and ordenadas(pura) == ordenadas(memo)
        linhas.append([n, alvo, milhar(len(memo)), milhar(m_pura.chamadas), milhar(m_memo.chamadas),
                       f"×{decimal(m_pura.chamadas / m_memo.chamadas)}", f"{decimal(t_pura, 3)} s", f"{decimal(t_memo, 3)} s"])
    tabela(["n", "alvo", "soluções", "chamadas (pura)", "chamadas (memo)", "redução", "tempo (pura)", "tempo (memo)"],
           linhas, ">>>>>>>>")
    ok(iguais, "as duas versões devolvem exatamente as mesmas combinações em todos os tamanhos")


def mostrar_contagem():
    titulo("Só contando as soluções (contar_combinacoes, com memo): a recursão pura seria inviável")
    linhas = []
    for n in TAMANHOS + TAMANHOS_SO_MEMO:
        alvo, pesos = pesos_sequenciais(n)
        memo = {}
        quantidade, metricas = medir(contar_combinacoes, alvo, pesos, 0, memo)
        linhas.append([n, milhar(alvo), milhar(quantidade), milhar(metricas.chamadas), milhar(len(memo)),
                       milhar(n * (alvo + 1)), f"≈ 2^{n + 1}"])
    tabela(["n", "alvo", "soluções", "chamadas (memo)", "estados guardados", "estados possíveis n·(alvo+1)",
            "pura, pior caso"], linhas, ">>>>>>>")
    print("com n = 100 a recursão pura faria até 2,5 · 10^30 chamadas; a memoizada fez menos de 300 mil")


def mostrar_verificacoes():
    titulo("Verificações")
    gerador = random.Random(SEMENTE)
    casos = [(gerador.randint(0, 50), [gerador.randint(1, 12) for _ in range(gerador.randint(0, 14))]) for _ in range(150)]
    ok(all(ordenadas(knapsack(a, p)) == ordenadas(knapsack_memo(a, p)) for a, p in casos),
       f"memo e pura iguais em {len(casos)} conjuntos aleatórios (com pesos repetidos)")
    ok(all(contar_combinacoes(a, p) == len(knapsack(a, p)) for a, p in casos), "a contagem confere com a listagem")
    ok(all(medir(knapsack_memo, a, p)[1].chamadas <= 2 * len(p) * (a + 1) + 1 for a, p in casos),
       "chamadas da versão memo ≤ 2·n·(alvo + 1) + 1: cada estado é resolvido uma vez e chama no máximo 2")


def main():
    mostrar_comparacao()
    print()
    mostrar_contagem()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
