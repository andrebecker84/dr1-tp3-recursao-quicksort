"""Problema da mochila: recursão pura (Exercício 6) e memoização (Exercício 8).

Uma combinação é um conjunto de itens: dois pesos iguais em posições diferentes são itens diferentes.
"""
from algoritmos.metricas import Metricas


def _exigir_pesos(target, weights):
    if isinstance(target, bool) or not isinstance(target, int):
        raise ValueError("target deve ser inteiro")
    if any(isinstance(p, bool) or not isinstance(p, int) or p <= 0 for p in weights):
        raise ValueError("os pesos devem ser inteiros positivos")


def knapsack(target, weights, index=0, metricas=None, ao_visitar=None, nivel=1):
    """Todas as combinações de weights[index:] que somam exatamente target. O(2^n).

    Cada peso entra (o alvo diminui) ou fica de fora (o alvo continua), e a recursão segue no
    próximo índice. Casos base: alvo 0 é uma solução; alvo negativo ou pesos esgotados, nenhuma.
    """
    if nivel == 1:
        _exigir_pesos(target, weights)
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    if ao_visitar:
        ao_visitar(target, index, nivel)
    if target == 0:
        return [[]]
    if target < 0 or index == len(weights):
        return []
    peso = weights[index]
    com_ele = [[peso] + resto for resto in knapsack(target - peso, weights, index + 1, metricas, ao_visitar, nivel + 1)]
    sem_ele = knapsack(target, weights, index + 1, metricas, ao_visitar, nivel + 1)
    return com_ele + sem_ele


def knapsack_memo(target, weights, index=0, memo=None, metricas=None, nivel=1):
    """A mesma recursão, guardando o resultado de cada estado (alvo, índice) já resolvido. O(n · target) estados.

    Um estado depende só do alvo que falta e do índice: quem chega a ele por outro caminho recebe
    a resposta pronta, sem refazer a subárvore.
    """
    if nivel == 1:
        _exigir_pesos(target, weights)
    memo = {} if memo is None else memo
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    if target == 0:
        return [[]]
    if target < 0 or index == len(weights):
        return []
    estado = (target, index)
    if estado in memo:
        return memo[estado]
    peso = weights[index]
    com_ele = [[peso] + resto for resto in knapsack_memo(target - peso, weights, index + 1, memo, metricas, nivel + 1)]
    sem_ele = knapsack_memo(target, weights, index + 1, memo, metricas, nivel + 1)
    memo[estado] = com_ele + sem_ele
    return memo[estado]


def contar_combinacoes(target, weights, index=0, memo=None, metricas=None, nivel=1):
    """Quantas combinações somam target, com memoização. Sem listar as soluções, o custo é só o dos estados."""
    if nivel == 1:
        _exigir_pesos(target, weights)
    memo = {} if memo is None else memo
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    if target == 0:
        return 1
    if target < 0 or index == len(weights):
        return 0
    estado = (target, index)
    if estado not in memo:
        memo[estado] = (contar_combinacoes(target - weights[index], weights, index + 1, memo, metricas, nivel + 1)
                        + contar_combinacoes(target, weights, index + 1, memo, metricas, nivel + 1))
    return memo[estado]
