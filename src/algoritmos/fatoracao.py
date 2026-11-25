"""Fatoração recursiva de inteiros (Exercício 2)."""
from math import isqrt

from algoritmos.metricas import Metricas, avisar


def factor(x, lowest=2, metricas=None, rastro=None, nivel=1):
    """Fatores primos de x em ordem crescente; o produto da lista é sempre x.

    Procura um divisor d entre lowest e √x. Achou: d entra na lista e a recursão segue com x // d,
    a partir do próprio d. Não achou: x é primo e é o último fator. Casos especiais: negativo
    ganha o fator −1, factor(1) é [] (produto vazio) e factor(0) é [0], que não tem fatoração.
    """
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError("x deve ser inteiro")
    if not isinstance(lowest, int) or lowest < 2:
        raise ValueError("lowest deve ser um inteiro maior ou igual a 2")
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    if x < 0:
        avisar(rastro, "base", nivel, f"factor({x}): negativo, separa o −1")
        return [-1] + factor(-x, lowest, metricas, rastro, nivel + 1)
    if x < 2:
        avisar(rastro, "base", nivel, f"factor({x}): caso especial")
        return [0] if x == 0 else []
    limite = isqrt(x)
    for divisor in range(lowest, limite + 1):
        metricas.divisoes += 1
        if x % divisor == 0:
            avisar(rastro, "chamada", nivel, f"factor({x}, {lowest}): {divisor} divide, segue com {x // divisor}")
            return [divisor] + factor(x // divisor, divisor, metricas, rastro, nivel + 1)
    avisar(rastro, "base", nivel, f"factor({x}, {lowest}): nenhum divisor até √{x} ≈ {limite}, {x} é primo")
    return [x]
