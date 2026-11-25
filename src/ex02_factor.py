"""Exercício 2: fatoração recursiva com divisores entre lowest e a raiz quadrada de x."""
from algoritmos.fatoracao import factor
from algoritmos.metricas import medir
from apresentacao.terminal import compacta, imprimir_rastro, milhar, ok, tabela, titulo
from verificacao import fatoracao_correta

EXEMPLO = 360
ENTRADAS = (0, 1, -1, 2, 12, -12, 97, 360, 1_024, 1_000_003, 600_851_475_143)
INTERVALO_CONFERIDO = range(-1_000, 20_001)


def tentativas_sem_limites(fatores):
    """Tentativas se cada chamada recomeçasse do 2 e fosse até o próprio x: 2..p para cada fator p."""
    return sum(f - 1 for f in fatores if f > 1)


def mostrar_rastro():
    titulo(f"Exercício 2: factor({EXEMPLO}), cada divisor encontrado é uma chamada nova a partir dele")
    fatores = factor(EXEMPLO, rastro=imprimir_rastro)
    print(f"resultado: {compacta(fatores)} · a busca recomeça do último divisor (lowest), nunca do 2")


def mostrar_entradas():
    titulo("Entradas diferentes: especiais, primos, potências e compostos grandes")
    linhas = []
    for x in ENTRADAS:
        fatores, metricas = medir(factor, x)
        linhas.append([milhar(x), compacta(fatores), metricas.chamadas, milhar(metricas.divisoes),
                       milhar(tentativas_sem_limites(fatores))])
    tabela(["x", "factor(x)", "chamadas", "tentativas (lowest..√x)", "tentativas (2..x)"], linhas, ">>>>>")
    print("0 não tem fatoração ([0]); 1 é o produto vazio ([]); negativo ganha o fator -1")


def mostrar_verificacoes():
    titulo("Verificações")
    ok(all(fatoracao_correta(x, factor(x)) for x in INTERVALO_CONFERIDO),
       f"produto = x, fatores primos e em ordem crescente para os {milhar(len(INTERVALO_CONFERIDO))} inteiros "
       f"de {milhar(INTERVALO_CONFERIDO[0])} a {milhar(INTERVALO_CONFERIDO[-1])}")
    primo, metricas = medir(factor, 1_000_003)
    ok(primo == [1_000_003] and metricas.divisoes == 999,
       "primo 1.000.003: 999 tentativas (2 a 1.000), contra 1.000.002 sem o limite da raiz")
    try:
        factor(10, lowest=1)
        recusou = False
    except ValueError:
        recusou = True
    ok(recusou, "lowest < 2 é recusado: 1 divide qualquer número e a recursão nunca terminaria")


def main():
    mostrar_rastro()
    print()
    mostrar_entradas()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
