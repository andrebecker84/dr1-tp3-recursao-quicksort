"""Exercício 5: geração recursiva de todos os times de k candidatos."""
from math import comb

from algoritmos.combinacoes import teams
from algoritmos.metricas import medir
from apresentacao.terminal import milhar, ok, tabela, titulo
from verificacao import times_de_referencia

CANDIDATOS = "ABCDE"
K = 3
GRANDE = "ABCDEFGHIJKLMNOP"
LARGURA_DA_LISTA = 66


def resumir(times):
    texto = " ".join(time or "''" for time in times)
    return texto if len(texto) <= LARGURA_DA_LISTA else texto[:LARGURA_DA_LISTA - 4] + " ..."


def mostrar_exemplo():
    titulo(f"Exercício 5: teams('{CANDIDATOS}', {K}), cada candidato entra ou fica de fora")
    times, metricas = medir(teams, CANDIDATOS, K)
    primeiro, resto = CANDIDATOS[0], CANDIDATOS[1:]
    com_ele = [primeiro + time for time in teams(resto, K - 1)]
    sem_ele = teams(resto, K)
    tabela(["decisão sobre o 'A'", "subproblema", "times"], [
        ["A entra", f"'A' + teams('{resto}', {K - 1})", " ".join(com_ele)],
        ["A fica de fora", f"teams('{resto}', {K})", " ".join(sem_ele)],
    ], "<<<")
    print(f"{len(times)} times = C(5, 3) = {comb(5, 3)}, em {metricas.chamadas} chamadas")


def mostrar_valores_de_k():
    titulo(f"teams('{CANDIDATOS}', k) para todos os k")
    linhas = []
    for k in range(len(CANDIDATOS) + 2):
        times, metricas = medir(teams, CANDIDATOS, k)
        linhas.append([k, len(times), comb(len(CANDIDATOS), k), metricas.chamadas, resumir(times)])
    tabela(["k", "times", "C(5, k)", "chamadas", "times gerados"], linhas, ">>>><")
    print("k = 0: um único time vazio (''); k maior que o número de candidatos: nenhum time")


def mostrar_crescimento():
    titulo(f"Candidatos '{GRANDE}' (n = {len(GRANDE)}): quantidade de times e de chamadas")
    linhas = []
    for k in (1, 2, 4, 8, 12, 16):
        times, metricas = medir(teams, GRANDE, k)
        linhas.append([k, milhar(len(times)), milhar(comb(len(GRANDE), k)), milhar(metricas.chamadas)])
    tabela(["k", "times", "C(16, k)", "chamadas"], linhas, ">>>>")


def mostrar_verificacoes():
    titulo("Verificações")
    casos = [(GRANDE[:n], k) for n in range(11) for k in range(n + 2)]
    ok(all(teams(c, k) == times_de_referencia(c, k) for c, k in casos),
       f"mesmos times, na mesma ordem, do itertools.combinations em {len(casos)} casos (n de 0 a 10)")
    times = teams(GRANDE, 8)
    ok(len(set(times)) == len(times) == comb(16, 8), f"{milhar(len(times))} times de 8 entre 16, nenhum repetido")
    ok(teams("ABCA", 2) == ["AB", "AC", "BC"], "candidato repetido conta uma vez: teams('ABCA', 2) = AB AC BC")


def main():
    mostrar_exemplo()
    print()
    mostrar_valores_de_k()
    print()
    mostrar_crescimento()
    print()
    mostrar_verificacoes()


if __name__ == "__main__":
    main()
