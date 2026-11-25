"""Exercício 9: QuickSort recursivo com o último elemento como pivô."""
import random
import sys

from algoritmos.metricas import medir
from algoritmos.ordenacao import quicksort
from apresentacao.terminal import compacta, cor, milhar, ok, recuo, tabela, titulo
from dados import ARRAY_DO_LIVRO, SEMENTE, Cenario, lista_no_cenario
from verificacao import ordenacao_correta

sys.setrecursionlimit(10_000)       # entrada ordenada empilha N chamadas; o limite padrão do Python é 1.000

CENARIOS = (Cenario.ORDENADA, Cenario.INVERTIDA, Cenario.ALEATORIA)
TAMANHOS = (10, 100, 1_000, 2_000)


def imprimir_particao(lista, inicio, fim, pivo, nivel):
    """Callback do QuickSort: o trecho particionado, com o pivô já no lugar entre os dois lados."""
    esquerda, direita = compacta(lista[inicio:pivo]), compacta(lista[pivo + 1:fim + 1])
    print(f"{recuo(nivel)}{cor('36', f'[{inicio}..{fim}]')} pivô {cor('1;33', lista[pivo])}: "
          f"{esquerda} {cor('1;33', lista[pivo])} {direita}")


def mostrar_passo_a_passo():
    titulo(f"Exercício 9: quicksort({compacta(ARRAY_DO_LIVRO)}), cada linha é uma partição; o recuo é o nível")
    ordenada = quicksort(ARRAY_DO_LIVRO, ao_particionar=imprimir_particao)
    print(f"resultado: {compacta(ordenada)} · trechos com 0 ou 1 elemento são o caso base e não aparecem")


def mostrar_cenarios():
    titulo("Ordenados, invertidos e aleatórios")
    linhas, corretos = [], True
    for n in TAMANHOS:
        for cenario in CENARIOS:
            entrada = lista_no_cenario(n, cenario)
            saida, metricas = medir(quicksort, entrada)
            corretos = corretos and ordenacao_correta(entrada, saida)
            linhas.append([milhar(n), cenario, milhar(metricas.comparacoes), milhar(metricas.chamadas),
                           milhar(metricas.profundidade)])
    tabela(["N", "entrada", "comparações", "chamadas", "profundidade"], linhas, "><>>>")
    ok(corretos, f"as {len(linhas)} saídas estão em ordem e têm os mesmos elementos da entrada")
    print("ordenada e invertida: o pivô (último) é sempre o maior ou o menor, um lado fica vazio e a pilha chega a N")


def mostrar_verificacoes():
    titulo("Verificações")
    gerador = random.Random(SEMENTE)
    casos = [[gerador.randint(0, gerador.choice((1, 5, 100))) for _ in range(gerador.randint(0, 60))]
             for _ in range(2_000)]
    ok(all(quicksort(c) == sorted(c) for c in casos),
       f"igual ao sorted() em {milhar(len(casos))} listas aleatórias com repetidos (tamanhos 0 a 60)")
    entrada = list(ARRAY_DO_LIVRO)
    quicksort(entrada)
    ok(entrada == list(ARRAY_DO_LIVRO), "a lista de entrada não é alterada: a ordenação acontece numa cópia")
    ok(quicksort([]) == [] and quicksort([7]) == [7] and quicksort([7] * 50) == [7] * 50,
       "lista vazia, unitária e com todos os valores iguais")


def main():
    mostrar_passo_a_passo()
    print()
    mostrar_cenarios()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
