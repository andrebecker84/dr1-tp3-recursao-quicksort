"""Exercício 4: travessia recursiva de diretórios, com a profundidade mostrada pela indentação."""
import os
import tempfile

from algoritmos.diretorios import arquivos_por_nivel, percorrer
from algoritmos.metricas import medir
from apresentacao.terminal import cor, ok, tabela, titulo
from dados import criar_arvore
from verificacao import contar_com_os_walk

RAIZ_DO_EXEMPLO = "projeto"


def ultimos(itens):
    """Para cada item, se ele é o último da sua pasta: lido de trás para a frente, o primeiro visto em cada nível."""
    marcas, visto = [], {}
    for item in reversed(itens):
        marcas.append(item.nivel not in visto)
        visto = {nivel: True for nivel in visto if nivel < item.nivel}
        visto[item.nivel] = True
    return marcas[::-1]


def linhas_da_arvore(itens):
    """Um recuo de 4 colunas por nível, com as guias de cada pasta-mãe; diretórios em azul, com barra no fim."""
    fechados = {}
    for item, ultimo in zip(itens, ultimos(itens)):
        guias = "".join("    " if fechados[nivel] else "│   " for nivel in range(1, item.nivel))
        fechados[item.nivel] = ultimo
        nome = cor("1;34", item.nome + "/") if item.diretorio else item.nome
        yield f"{cor('2', str(item.nivel))}  {cor('2', guias + ('└── ' if ultimo else '├── '))}{nome}"


def mostrar_arvore(caminho):
    titulo(f"Exercício 4: percorrer('{RAIZ_DO_EXEMPLO}/'), um nível por chamada, a indentação é a profundidade")
    itens, metricas = medir(percorrer, caminho)
    print(f"{cor('2', '0')}  {cor('1;34', RAIZ_DO_EXEMPLO + '/')}")
    for linha in linhas_da_arvore(itens):
        print(linha)
    diretorios = sum(item.diretorio for item in itens)
    print(f"{metricas.chamadas} chamadas: 1 para a raiz e 1 para cada um dos {diretorios} subdiretórios "
          f"· profundidade máxima {metricas.profundidade}")
    return itens


def mostrar_por_nivel(itens):
    titulo("Arquivos encontrados em cada nível")
    linhas = [[nivel, len(nomes), ", ".join(nomes)] for nivel, nomes in sorted(arquivos_por_nivel(itens).items())]
    tabela(["nível", "arquivos", "nomes"], linhas, "><<")


def mostrar_pasta_real():
    titulo("A mesma função sobre uma pasta real: o src/ deste trabalho")
    itens, metricas = medir(percorrer, ".")
    linhas = [[nivel, len(nomes)] for nivel, nomes in sorted(arquivos_por_nivel(itens).items())]
    tabela(["nível", "arquivos"], linhas, ">>")
    arquivos = sum(not item.diretorio for item in itens)
    print(f"{arquivos} arquivos em {metricas.chamadas} diretórios (src/ e {metricas.chamadas - 1} subdiretórios)")


def mostrar_verificacoes(caminho, itens):
    titulo("Verificações (o os.walk só confere, não faz a travessia)")
    arquivos = sum(not item.diretorio for item in itens)
    diretorios = sum(item.diretorio for item in itens)
    ok((arquivos, diretorios) == contar_com_os_walk(caminho),
       f"{arquivos} arquivos e {diretorios} diretórios, os mesmos números do os.walk")
    posicao = next(i for i, item in enumerate(itens) if item.nome == "vazio")
    abaixo = itens[posicao + 1:posicao + 2]
    ok(itens[posicao].diretorio and not (abaixo and abaixo[0].nivel > itens[posicao].nivel),
       "vazio/ aparece, e a chamada sobre ele não acha nada e retorna: o caso base da descida")
    ok(contar_com_os_walk(".")[0] == sum(not item.diretorio for item in percorrer(".")),
       "na pasta real, o mesmo total de arquivos do os.walk")


def main():
    with tempfile.TemporaryDirectory() as temporaria:
        caminho = os.path.join(temporaria, RAIZ_DO_EXEMPLO)
        criar_arvore(caminho)
        itens = mostrar_arvore(caminho)
        print()
        mostrar_por_nivel(itens)
        print()
        mostrar_pasta_real()
        print()
        mostrar_verificacoes(caminho, itens)


if __name__ == "__main__":
    main()
