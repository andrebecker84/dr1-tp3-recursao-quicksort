"""Travessia recursiva de diretórios (Exercício 4).

os.scandir lê um único nível; a descida aos subdiretórios é feita pela própria recursão. Nada de
os.walk, glob('**') ou Path.rglob, que já percorrem a árvore inteira sozinhos.
"""
import os
from collections import namedtuple

from algoritmos.metricas import Metricas

Item = namedtuple("Item", "nivel nome diretorio")


def _ordem(entrada):
    """Arquivos primeiro, depois subdiretórios, cada grupo em ordem alfabética: a saída não muda entre execuções."""
    return (entrada.is_dir(follow_symlinks=False), entrada.name.lower())


def percorrer(caminho, nivel=1, metricas=None):
    """Itens de caminho e de todos os subdiretórios, em pré-ordem: o diretório e logo abaixo o seu conteúdo.

    O nível de cada item é a distância até a raiz: o conteúdo de caminho está no nível 1.

    O caso base é implícito: um diretório sem subdiretórios não faz nenhuma chamada nova. Links
    simbólicos não são seguidos, o que evita ciclos.
    """
    metricas = metricas or Metricas()
    metricas.entrar(nivel)
    try:
        with os.scandir(caminho) as leitura:
            entradas = sorted(leitura, key=_ordem)
    except PermissionError:
        return [Item(nivel, "[sem permissão de leitura]", False)]
    itens = []
    for entrada in entradas:
        if entrada.is_dir(follow_symlinks=False):
            itens.append(Item(nivel, entrada.name, True))
            itens += percorrer(entrada.path, nivel + 1, metricas)
        else:
            itens.append(Item(nivel, entrada.name, False))
    return itens


def arquivos_por_nivel(itens):
    """{nível: [nomes dos arquivos]} a partir do resultado de percorrer."""
    por_nivel = {}
    for item in itens:
        if not item.diretorio:
            por_nivel.setdefault(item.nivel, []).append(item.nome)
    return por_nivel
