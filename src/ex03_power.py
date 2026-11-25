"""Exercício 3: potenciação recursiva com expoentes positivos, negativos e zero."""
import math
import sys

from algoritmos.aritmetica import power, power_linear
from algoritmos.metricas import medir
from apresentacao.terminal import cor, milhar, ok, tabela, titulo

sys.setrecursionlimit(10_000)       # a versão linear empilha y quadros; o limite padrão do Python é 1.000

CASOS = ((2, 10), (3, 5), (5, 0), (7, 1), (2, -3), (-2, -3), (10, -2), (-3, 3), (1.5, 2), (0, 0), (0, 5), (0, -1))
EXPOENTES = (1, 2, 10, 100, 1_000, 5_000)
EXPOENTES_SO_LOG = (100_000, 1_000_000)


def descrever(x, y):
    try:
        return power(x, y), f"{x ** y!r}"
    except ZeroDivisionError:
        return cor("1;31", "ZeroDivisionError"), "ZeroDivisionError"


def mostrar_casos():
    titulo("Exercício 3: power(x, y) com expoentes positivos, negativos e zero")
    linhas = []
    for x, y in CASOS:
        resultado, referencia = descrever(x, y)
        tipo = "base y = 0" if y == 0 else "base y = 1" if y == 1 else "negativo: 1 / x^|y|" if y < 0 else "positivo"
        linhas.append([x, y, tipo, resultado, referencia])
    tabela(["x", "y", "caso", "power(x, y)", "x ** y do Python"], linhas, ">><>>")
    print("0 ** -1 não existe (seria 1 / 0): power levanta ZeroDivisionError, como o próprio Python")


def mostrar_complexidade():
    titulo("Multiplicações: quadrados sucessivos O(log y) x versão linear O(y), para x = 2")
    linhas = []
    for y in EXPOENTES + EXPOENTES_SO_LOG:
        _, rapida = medir(power, 2, y)
        linear = milhar(medir(power_linear, 2, y)[1].multiplicacoes) if y in EXPOENTES else "estoura a pilha"
        linhas.append([milhar(y), rapida.chamadas, rapida.multiplicacoes, 2 * math.floor(math.log2(y)), linear])
    tabela(["y", "chamadas", "multiplicações", "limite 2·⌊log₂ y⌋", "linear (y − 1)"], linhas, ">>>>>")
    print("dobrar y acrescenta uma chamada à versão rápida e dobra o trabalho da linear")


def mostrar_verificacoes():
    titulo("Verificações")
    pares = [(x, y) for x in (-3, -2, -1, 0, 1, 2, 3, 0.5, 1.5) for y in range(-12, 41) if not (x == 0 and y < 0)]
    ok(all(math.isclose(power(x, y), x ** y) for x, y in pares),
       f"power(x, y) igual a x ** y nos {len(pares)} pares com -12 <= y <= 40 (bases inteiras, negativas e reais)")
    ok(all(medir(power, 2, y)[1].multiplicacoes <= 2 * math.floor(math.log2(y)) for y in range(1, 5_001)),
       "no máximo 2·⌊log₂ y⌋ multiplicações para todo y de 1 a 5.000")
    ok(power(2, -3) == 0.125 and power(5, 0) == 1 and power(7, 1) == 7,
       "casos base: x^0 = 1 e x^1 = x; expoente negativo vira 1 / x^|y| (2^-3 = 0,125)")


def main():
    mostrar_casos()
    print()
    mostrar_complexidade()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
