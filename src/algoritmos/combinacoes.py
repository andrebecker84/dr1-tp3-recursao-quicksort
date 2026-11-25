"""Combinações (times) com recursão de inclusão e exclusão (Exercício 5)."""
from algoritmos.metricas import Metricas


def sem_repetidos(candidates):
    """Cada candidato uma vez, na ordem em que aparece: "ABCA" vira "ABC"."""
    vistos = {}
    for candidato in candidates:
        vistos.setdefault(candidato, True)
    return "".join(vistos)


def teams(candidates, k, metricas=None, nivel=1):
    """Todos os times de k candidatos, cada um como string, na ordem da entrada.

    Decisão sobre o primeiro candidato: ou ele entra (e faltam k − 1 entre os demais) ou fica de
    fora (e os k saem dos demais). Cada candidato é decidido uma única vez por caminho, então
    nenhum time se repete. Casos base: k = 0 é um time completo; menos candidatos que k, nenhum.
    """
    if nivel == 1:
        if isinstance(k, bool) or not isinstance(k, int) or k < 0:
            raise ValueError("k deve ser um inteiro maior ou igual a zero")
        candidates = sem_repetidos(candidates)
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    if k == 0:
        return [""]
    if len(candidates) < k:
        return []
    primeiro, resto = candidates[0], candidates[1:]
    com_ele = [primeiro + time for time in teams(resto, k - 1, metricas, nivel + 1)]
    sem_ele = teams(resto, k, metricas, nivel + 1)
    return com_ele + sem_ele
