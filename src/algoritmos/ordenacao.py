"""Partição com o último elemento como pivô, QuickSort (Exercícios 9 e 10) e QuickSelect (Exercício 11).

As duas funções públicas trabalham numa cópia e não alteram a entrada. Contagem: cada comparação de
um elemento com o pivô vale 1; cada troca vale 3 cópias (temp = a; a = b; b = temp).
"""
from algoritmos.metricas import Metricas


def trocar(lista, i, j, metricas):
    """Troca com variável temporária: 3 cópias. Trocar uma posição com ela mesma não move nada."""
    if i == j:
        return
    temp = lista[i]
    lista[i] = lista[j]
    lista[j] = temp
    metricas.copias += 3


def particionar(lista, inicio, fim, metricas):
    """Separa lista[inicio..fim] em torno do pivô lista[fim]. Devolve a posição final do pivô.

    O ponteiro da esquerda avança enquanto acha menores que o pivô; o da direita recua enquanto
    acha maiores. Quando os dois param, os valores trocam de lado. Quando se cruzam, o pivô vai
    para onde o da esquerda parou: à esquerda dele só ficam menores ou iguais, à direita maiores ou iguais.
    """
    pivo = lista[fim]
    esquerda, direita = inicio, fim - 1
    while True:
        while esquerda < fim:
            metricas.comparacoes += 1
            if lista[esquerda] >= pivo:
                break
            esquerda += 1
        while direita > inicio:
            metricas.comparacoes += 1
            if lista[direita] <= pivo:
                break
            direita -= 1
        if esquerda >= direita:
            break
        trocar(lista, esquerda, direita, metricas)
        esquerda += 1
        direita -= 1
    trocar(lista, esquerda, fim, metricas)
    return esquerda


def _quicksort(lista, inicio, fim, metricas, ao_particionar, nivel):
    metricas.entrar(nivel)
    if fim - inicio < 1:                    # caso base: 0 ou 1 elemento já está ordenado
        return
    pivo = particionar(lista, inicio, fim, metricas)
    if ao_particionar:
        ao_particionar(lista, inicio, fim, pivo, nivel)
    _quicksort(lista, inicio, pivo - 1, metricas, ao_particionar, nivel + 1)
    _quicksort(lista, pivo + 1, fim, metricas, ao_particionar, nivel + 1)


def quicksort(seq, metricas=None, ao_particionar=None):
    """Ordena uma cópia: particiona e ordena, recursivamente, os dois lados do pivô.

    Melhor e caso médio O(N log N); pior caso O(N²), quando o pivô é sempre o menor ou o maior.
    """
    metricas = metricas or Metricas()
    lista = list(seq)
    _quicksort(lista, 0, len(lista) - 1, metricas, ao_particionar, 1)
    return lista


def _quickselect(lista, inicio, fim, k, metricas, ao_particionar, nivel):
    metricas.entrar(nivel)
    if inicio == fim:                       # caso base: sobrou um elemento, e ele é o procurado
        return lista[inicio]
    pivo = particionar(lista, inicio, fim, metricas)
    if ao_particionar:
        ao_particionar(lista, inicio, fim, pivo, nivel)
    if pivo == k:                           # o pivô caiu na posição procurada: para aqui
        return lista[pivo]
    if k < pivo:
        return _quickselect(lista, inicio, pivo - 1, k, metricas, ao_particionar, nivel + 1)
    return _quickselect(lista, pivo + 1, fim, k, metricas, ao_particionar, nivel + 1)


def quickselect(seq, k, metricas=None, ao_particionar=None):
    """O valor que ocupa o índice k da lista ordenada, sem ordenar a lista toda.

    Só o lado que contém k é visitado. Caso médio O(N); pior caso O(N²).
    """
    if isinstance(k, bool) or not isinstance(k, int) or not 0 <= k < len(seq):
        raise IndexError(f"k deve estar entre 0 e {len(seq) - 1}")
    metricas = metricas or Metricas()
    lista = list(seq)
    return _quickselect(lista, 0, len(lista) - 1, k, metricas, ao_particionar, 1)


def mediana(seq, metricas=None):
    """Mediana com o QuickSelect: o elemento central, ou a média dos dois centrais quando N é par."""
    n = len(seq)
    if n % 2:
        return quickselect(seq, n // 2, metricas)
    return (quickselect(seq, n // 2 - 1, metricas) + quickselect(seq, n // 2, metricas)) / 2
