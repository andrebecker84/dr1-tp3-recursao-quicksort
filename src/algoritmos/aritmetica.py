"""Multiplicação só com somas (Exercício 1) e potenciação com expoente negativo (Exercício 3)."""
from algoritmos.metricas import Metricas, avisar


def _exigir_natural(y, nome="y"):
    if isinstance(y, bool) or not isinstance(y, int) or y < 0:
        raise ValueError(f"{nome} deve ser um inteiro maior ou igual a zero")


def mult(x, y, metricas=None, rastro=None, nivel=1):
    """x · y só com somas: mult(x, y) = x + mult(x, y − 1), com caso base mult(x, 0) = 0. O(y)."""
    if nivel == 1:
        _exigir_natural(y)
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    avisar(rastro, "chamada", nivel, f"mult({x}, {y})")
    if y == 0:
        avisar(rastro, "base", nivel, "caso base y = 0: devolve 0")
        return 0
    parcial = mult(x, y - 1, metricas, rastro, nivel + 1)
    resultado = x + parcial                 # a soma só acontece aqui, quando a chamada de baixo retorna
    metricas.somas += 1
    avisar(rastro, "retorno", nivel, f"{x} + {parcial} = {resultado}")
    return resultado


def mult_acumulando(x, y, acumulado=0, metricas=None, rastro=None, nivel=1):
    """A mesma conta com a soma feita na ida: o resultado parcial desce como parâmetro. O(y)."""
    if nivel == 1:
        _exigir_natural(y)
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    avisar(rastro, "chamada", nivel, f"mult_acumulando({x}, {y}, acumulado={acumulado})")
    if y == 0:
        avisar(rastro, "base", nivel, f"caso base y = 0: devolve o acumulado {acumulado}")
        return acumulado
    metricas.somas += 1                     # a soma acontece antes da chamada, no argumento
    resultado = mult_acumulando(x, y - 1, acumulado + x, metricas, rastro, nivel + 1)
    avisar(rastro, "retorno", nivel, f"repassa {resultado}, sem nenhuma conta")
    return resultado


def power(x, y, metricas=None, nivel=1):
    """x elevado a y por quadrados sucessivos: x^y = (x²)^(y // 2), vezes x se y for ímpar. O(log y).

    Expoente negativo: x^(−y) = 1 / x^y. Casos base: y = 0 devolve 1 e y = 1 devolve x.
    """
    if isinstance(y, bool) or not isinstance(y, int):
        raise ValueError("o expoente deve ser inteiro")
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    if y < 0:
        if x == 0:
            raise ZeroDivisionError("0 elevado a um expoente negativo não está definido")
        metricas.divisoes += 1
        return 1 / power(x, -y, metricas, nivel + 1)
    if y == 0:
        return 1
    if y == 1:
        return x
    metricas.multiplicacoes += 1            # x · x, calculado na ida
    metade = power(x * x, y // 2, metricas, nivel + 1)
    if y % 2 == 0:
        return metade
    metricas.multiplicacoes += 1            # o x que sobra quando y é ímpar, na volta
    return metade * x


def power_linear(x, y, metricas=None, nivel=1):
    """Versão direta, só para comparar: x^y = x · x^(y − 1). O(y) chamadas e multiplicações."""
    _exigir_natural(y)
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    if y == 0:
        return 1
    if y == 1:
        return x
    resultado = x * power_linear(x, y - 1, metricas, nivel + 1)
    metricas.multiplicacoes += 1
    return resultado
