"""Exercício 12: QuickSort x QuickSelect sobre os mesmos dados, para achar a mediana."""
import sys

from algoritmos.metricas import medir
from algoritmos.ordenacao import quickselect, quicksort
from apresentacao.terminal import decimal, milhar, ok, tabela, titulo
from dados import SEMENTE, Cenario, aleatorios, lista_no_cenario

sys.setrecursionlimit(10_000)

TAMANHOS = (1_001, 10_001, 100_001)
LISTAS_POR_TAMANHO = 10
N_PIOR_CASO = 2_001

CENARIOS_DE_USO = (
    ("mediana, k-ésimo menor, percentil", "QuickSelect", "O(N) médio: só o lado que contém k"),
    ("os k menores, sem ordem entre eles", "QuickSelect", "depois de achar o índice k, eles estão à esquerda"),
    ("saída ordenada ou listagem em ordem", "QuickSort", "a seleção não ordena os lados"),
    ("muitas consultas de posição", "QuickSort", "ordena uma vez e cada consulta custa O(1)"),
    ("entrada já (quase) ordenada", "nenhum com este pivô", "os dois caem em O(N²); trocar o pivô"),
)


def comparar(dados):
    k = len(dados) // 2
    ordenada, m_ordenacao = medir(quicksort, dados)
    selecionado, m_selecao = medir(quickselect, dados, k)
    return ordenada[k] == selecionado, m_ordenacao, m_selecao


def medias(n):
    """Comparações e cópias médias das duas versões em LISTAS_POR_TAMANHO listas aleatórias de tamanho n."""
    soma = [0, 0, 0, 0]
    iguais = True
    for semente in range(SEMENTE, SEMENTE + LISTAS_POR_TAMANHO):
        igual, ordenacao, selecao = comparar(aleatorios(n, semente))
        iguais = iguais and igual
        for i, valor in enumerate((ordenacao.comparacoes, selecao.comparacoes, ordenacao.copias, selecao.copias)):
            soma[i] += valor
    return iguais, [round(s / LISTAS_POR_TAMANHO) for s in soma]


def mostrar_aleatorios():
    titulo(f"Exercício 12: a mediana de listas aleatórias, ordenando tudo ou só selecionando "
           f"(média de {LISTAS_POR_TAMANHO} listas)")
    linhas, todas_iguais, razoes = [], True, []
    for n in TAMANHOS:
        iguais, (comp_ordenacao, comp_selecao, cop_ordenacao, cop_selecao) = medias(n)
        todas_iguais = todas_iguais and iguais
        razoes.append(comp_ordenacao / comp_selecao)
        linhas.append([milhar(n), milhar(comp_ordenacao), milhar(comp_selecao), f"×{decimal(razoes[-1])}",
                       milhar(cop_ordenacao), milhar(cop_selecao), f"×{decimal(cop_ordenacao / cop_selecao)}"])
    tabela(["N", "comparações QuickSort", "comparações QuickSelect", "razão", "cópias QuickSort",
            "cópias QuickSelect", "razão"], linhas, ">>>>>>>")
    ok(todas_iguais, f"nas {len(TAMANHOS) * LISTAS_POR_TAMANHO} listas, o QuickSelect devolve o elemento central "
                     "da lista ordenada pelo QuickSort")
    print(f"a razão cresce com N, como N log N ÷ N = log N: com N = 100.001, até {int(razoes[-1])} seleções avulsas "
          "custam menos que uma ordenação")


def mostrar_pior_caso():
    titulo(f"Entrada ordenada (N = {milhar(N_PIOR_CASO)}): o pivô no fim prejudica os dois")
    igual, ordenacao, selecao = comparar(lista_no_cenario(N_PIOR_CASO, Cenario.ORDENADA))
    n = N_PIOR_CASO
    tabela(["algoritmo", "comparações", "profundidade", "referência"], [
        ["QuickSort", milhar(ordenacao.comparacoes), milhar(ordenacao.profundidade), f"N²/2 = {milhar(n * n // 2)}"],
        ["QuickSelect", milhar(selecao.comparacoes), milhar(selecao.profundidade), f"3N²/8 = {milhar(3 * n * n // 8)}"],
    ], "<>>>")
    ok(igual, "mesmo resultado; o QuickSelect só para quando o pivô chega ao meio, depois de N/2 partições")


def mostrar_cenarios_de_uso():
    titulo("Qual usar")
    tabela(["objetivo", "algoritmo", "por quê"], CENARIOS_DE_USO, "<<<")


def main():
    mostrar_aleatorios()
    print()
    mostrar_pior_caso()
    print()
    mostrar_cenarios_de_uso()


if __name__ == "__main__":
    main()
