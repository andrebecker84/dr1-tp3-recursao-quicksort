"""Exercício 11: QuickSelect recursivo, com a partição do QuickSort, para qualquer índice e para a mediana."""
import random

from algoritmos.metricas import medir
from algoritmos.ordenacao import mediana, quickselect
from apresentacao.terminal import compacta, cor, decimal, milhar, ok, recuo, tabela, titulo
from dados import SEMENTE, aleatorios

EXEMPLO = (9, 4, 7, 1, 8, 2, 6, 5, 3)
TAMANHOS = (11, 101, 1_001, 10_001, 100_001)


def rastro_de_selecao(k):
    def imprimir(lista, inicio, fim, pivo, nivel):
        if pivo == k:
            decisao = cor("1;32", f"pivô no índice {pivo} = k: encontrado, a recursão para")
        else:
            lado = "esquerda" if k < pivo else "direita"
            decisao = f"pivô no índice {pivo}, k = {k} está à {lado}: só esse lado continua"
        print(f"{recuo(nivel)}{cor('36', f'[{inicio}..{fim}]')} {compacta(lista[inicio:fim + 1])} → {decisao}")
    return imprimir


def mostrar_passo_a_passo():
    k = len(EXEMPLO) // 2
    titulo(f"Exercício 11: quickselect({compacta(EXEMPLO)}, k = {k}), a mediana sem ordenar tudo")
    valor, metricas = medir(quickselect, EXEMPLO, k, ao_particionar=rastro_de_selecao(k))
    print(f"resultado: {valor} (ordenada seria {compacta(sorted(EXEMPLO))}) · {metricas.chamadas} chamadas, "
          f"{metricas.comparacoes} comparações")


def mostrar_qualquer_indice():
    titulo(f"Qualquer índice da mesma lista: k = 0 é o mínimo, k = {len(EXEMPLO) - 1} é o máximo")
    linhas = []
    for k in range(len(EXEMPLO)):
        valor, metricas = medir(quickselect, EXEMPLO, k)
        linhas.append([k, valor, metricas.chamadas, metricas.comparacoes, metricas.copias])
    tabela(["k", "valor", "chamadas", "comparações", "cópias"], linhas, ">>>>>")


def mostrar_medianas():
    titulo("Mediana de listas aleatórias (N ímpar: índice N // 2)")
    linhas, corretas = [], True
    for n in TAMANHOS:
        dados = aleatorios(n)
        valor, metricas = medir(quickselect, dados, n // 2)
        corretas = corretas and valor == sorted(dados)[n // 2]
        linhas.append([milhar(n), milhar(valor), milhar(metricas.chamadas), milhar(metricas.comparacoes),
                       decimal(metricas.comparacoes / n, 2)])
    tabela(["N", "mediana", "chamadas", "comparações", "comparações ÷ N"], linhas, ">>>>>")
    ok(corretas, "a mediana confere com a lista ordenada pelo sorted() em todos os tamanhos")
    print("comparações ÷ N oscila entre 1,7 e 4,5 e não cresce com N: custo linear, O(N), no caso médio")


def mostrar_verificacoes():
    titulo("Verificações")
    gerador = random.Random(SEMENTE)
    total = 0
    certo = True
    for _ in range(300):
        dados = [gerador.randint(0, gerador.choice((3, 50, 1_000))) for _ in range(gerador.randint(1, 40))]
        ordenados = sorted(dados)
        certo = certo and all(quickselect(dados, k) == ordenados[k] for k in range(len(dados)))
        total += len(dados)
    ok(certo, f"todos os {milhar(total)} índices de 300 listas aleatórias (com repetidos) iguais ao sorted()[k]")
    ok(mediana([4, 1, 3, 2]) == 2.5 and mediana([5]) == 5, "N par: média dos dois centrais (mediana([4 1 3 2]) = 2,5)")
    try:
        quickselect([3, 1, 2], 3)
        recusou = False
    except IndexError:
        recusou = True
    ok(recusou, "k fora de 0..N−1 é recusado antes de qualquer partição")


def main():
    mostrar_passo_a_passo()
    print()
    mostrar_qualquer_indice()
    print()
    mostrar_medianas()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
