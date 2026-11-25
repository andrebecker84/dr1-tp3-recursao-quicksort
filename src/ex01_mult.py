"""Exercício 1: multiplicação recursiva só com somas, com o rastro de chamadas e retornos."""
from algoritmos.aritmetica import mult, mult_acumulando
from algoritmos.metricas import medir
from apresentacao.terminal import cor, imprimir_rastro, milhar, ok, tabela, titulo

X, Y = 5, 4
VALORES_DE_Y = (0, 1, 2, 10, 100, 500)


def mostrar_rastro():
    titulo(f"Exercício 1: mult({X}, {Y}) só com somas: a soma acontece no retorno")
    resultado = mult(X, Y, rastro=imprimir_rastro)
    print(f"resultado: {resultado} · as {Y + 1} chamadas descem sem somar nada; as {Y} somas sobem com os retornos")


def mostrar_contraste():
    titulo(f"Contraste: mult_acumulando({X}, {Y}) soma na chamada e só repassa na volta")
    resultado = mult_acumulando(X, Y, rastro=imprimir_rastro)
    print(f"resultado: {resultado} · o parcial desce como argumento (0, 5, 10, 15, 20)")


def mostrar_crescimento():
    titulo(f"Custo de mult({X}, y): chamadas, somas e profundidade da pilha")
    linhas, conferido = [], True
    for y in VALORES_DE_Y:
        resultado, metricas = medir(mult, X, y)
        conferido = conferido and resultado == X * y and metricas.chamadas == y + 1 and metricas.somas == y
        linhas.append([y, milhar(resultado), metricas.chamadas, metricas.somas, metricas.profundidade])
    tabela(["y", "mult(5, y)", "chamadas", "somas", "profundidade"], linhas, ">>>>>")
    ok(conferido, "y + 1 chamadas, y somas e y + 1 quadros empilhados: O(y) em tempo e em memória")


def mostrar_verificacoes():
    titulo("Verificações")
    pares = [(x, y) for x in range(31) for y in range(31)]
    ok(all(mult(x, y) == x * y == mult_acumulando(x, y) for x, y in pares),
       f"mult e mult_acumulando iguais a x * y nos {len(pares)} pares com 0 <= x, y <= 30")
    try:
        mult(3, -2)
        recusou = False
    except ValueError as erro:
        recusou = True
        print(cor("2", f"mult(3, -2) → ValueError: {erro}"))
    ok(recusou, "y negativo é recusado: sem o caso base y = 0 no caminho, a recursão não pararia")


def main():
    mostrar_rastro()
    print()
    mostrar_contraste()
    print()
    mostrar_crescimento()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
