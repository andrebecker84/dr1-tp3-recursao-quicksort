"""Conferências usadas nos scripts e nos testes. Ficam fora do núcleo para não se misturarem à contagem.

Aqui podem aparecer as ferramentas prontas que os exercícios evitam (os.walk, itertools), porque
servem só de referência independente para conferir o resultado.
"""
import itertools
import os


def esta_ordenada(seq):
    return all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1))


def mesma_colecao(a, b):
    """Mesmos elementos com as mesmas quantidades, em qualquer ordem."""
    contagem = {}
    for valor in a:
        contagem[valor] = contagem.get(valor, 0) + 1
    for valor in b:
        contagem[valor] = contagem.get(valor, 0) - 1
    return all(quantidade == 0 for quantidade in contagem.values())


def ordenacao_correta(entrada, saida):
    """A saída está em ordem e é uma permutação da entrada."""
    return esta_ordenada(saida) and mesma_colecao(entrada, saida)


def produto(valores):
    resultado = 1
    for valor in valores:
        resultado *= valor
    return resultado


def e_primo(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def fatoracao_correta(x, fatores):
    """O produto dá x; sem o −1 inicial, os fatores são primos e estão em ordem crescente."""
    primos = fatores[1:] if fatores[:1] == [-1] else fatores
    if x == 0:
        return fatores == [0]
    return produto(fatores) == x and esta_ordenada(primos) and all(e_primo(f) for f in primos)


def contar_com_os_walk(caminho):
    """(arquivos, diretórios) abaixo de caminho, contados pelo os.walk, sem seguir links."""
    arquivos = diretorios = 0
    for _, subdiretorios, nomes in os.walk(caminho):
        arquivos += len(nomes)
        diretorios += len(subdiretorios)
    return arquivos, diretorios


def times_de_referencia(candidatos, k):
    return ["".join(time) for time in itertools.combinations(candidatos, k)]


def subconjuntos_que_somam(alvo, pesos):
    """Todos os subconjuntos (por posição) que somam alvo, enumerando as 2^n máscaras de bits."""
    n = len(pesos)
    return sorted(sorted(pesos[i] for i in range(n) if mascara >> i & 1)
                  for mascara in range(1 << n) if sum(pesos[i] for i in range(n) if mascara >> i & 1) == alvo)
