"""Exercício 10: comparações e cópias do QuickSort em diferentes tipos de entrada (troca = 3 cópias)."""
import math
import sys

from algoritmos.metricas import Metricas, medir
from algoritmos.ordenacao import quicksort
from apresentacao.terminal import compacta, decimal, milhar, ok, tabela, titulo
from dados import ARRAY_DO_LIVRO, Cenario, lista_no_cenario

sys.setrecursionlimit(10_000)

TAMANHOS = (100, 1_000, 2_000)


def mostrar_contagem_por_particao():
    titulo(f"Exercício 10: contadores a cada partição de {compacta(ARRAY_DO_LIVRO)}")
    metricas, linhas = Metricas(), []
    anterior = [0, 0]

    def registrar(lista, inicio, fim, pivo, _nivel):
        comparacoes, copias = metricas.comparacoes - anterior[0], metricas.copias - anterior[1]
        anterior[:] = [metricas.comparacoes, metricas.copias]
        linhas.append([f"[{inicio}..{fim}]", lista[pivo], comparacoes, copias // 3, copias,
                       compacta(lista[inicio:fim + 1])])

    quicksort(ARRAY_DO_LIVRO, metricas, registrar)
    tabela(["trecho", "pivô", "comparações", "trocas", "cópias", "trecho depois da partição"], linhas, "<>>>><")
    print(f"total: {metricas.comparacoes} comparações e {metricas.copias} cópias · a troca do pivô consigo mesmo "
          "não move nada e não conta")


def mostrar_cenarios():
    titulo("Comparações e cópias por tipo de entrada")
    linhas, resultados = [], {}
    for n in TAMANHOS:
        for cenario in Cenario:
            _, metricas = medir(quicksort, lista_no_cenario(n, cenario))
            resultados[(n, cenario)] = metricas
            linhas.append([milhar(n), cenario, milhar(metricas.comparacoes), milhar(metricas.copias),
                           decimal(metricas.comparacoes / (n * math.log2(n)), 2),
                           decimal(metricas.comparacoes / (n * n / 2), 3)])
    tabela(["N", "entrada", "comparações", "cópias", "comp ÷ N·log₂N", "comp ÷ N²/2"], linhas, "><>>>>")
    print("aleatória e muitos repetidos: ≈ 1·N·log₂N, O(N log N) · ordenada, invertida e quase ordenada: ≈ N²/2, O(N²)")
    return resultados


def mostrar_verificacoes(resultados):
    titulo("Verificações")
    ok(all(m.copias % 3 == 0 for m in resultados.values()), "toda cópia vem de uma troca: as cópias são múltiplas de 3")
    ok(all(resultados[(n, Cenario.ORDENADA)].comparacoes == n * (n + 1) // 2 - 2 for n in TAMANHOS)
       and all(resultados[(n, Cenario.ORDENADA)].copias == 0 for n in TAMANHOS),
       "ordenada: exatamente N(N+1)/2 − 2 comparações e nenhuma cópia (o pivô já está no lugar)")
    ok(all(resultados[(n, Cenario.INVERTIDA)].copias == 3 * (n // 2) for n in TAMANHOS),
       "invertida: só 3·⌊N/2⌋ cópias, mas o mesmo número quadrático de comparações")


def main():
    mostrar_contagem_por_particao()
    print()
    resultados = mostrar_cenarios()
    print()
    mostrar_verificacoes(resultados)


if __name__ == "__main__":
    main()
