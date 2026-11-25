"""Contadores das operações que dominam o custo: medimos passos, não tempo."""
from dataclasses import dataclass


@dataclass
class Metricas:
    chamadas: int = 0
    profundidade: int = 0       # maior número de chamadas empilhadas ao mesmo tempo
    somas: int = 0
    multiplicacoes: int = 0
    divisoes: int = 0           # tentativas de divisão na fatoração
    comparacoes: int = 0
    copias: int = 0             # uma troca conta 3 cópias (temp = a; a = b; b = temp)

    def entrar(self, nivel):
        """Registra uma chamada no nível nivel da pilha de recursão (a chamada inicial é o nível 1)."""
        self.chamadas += 1
        self.profundidade = max(self.profundidade, nivel)


def medir(algoritmo, *args, **kwargs):
    """Executa o algoritmo com contadores zerados e devolve (resultado, metricas)."""
    metricas = Metricas()
    return algoritmo(*args, metricas=metricas, **kwargs), metricas


def avisar(rastro, evento, nivel, texto):
    """Observer: repassa o evento ao rastro, se houver. O algoritmo não imprime nada."""
    if rastro:
        rastro(evento, nivel, texto)
