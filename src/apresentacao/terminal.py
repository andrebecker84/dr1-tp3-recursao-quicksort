"""Saída no terminal: títulos, tabelas, o resultado das verificações e o rastro da recursão."""
import os
import re
import sys

# Redirecionada para arquivo, a saída sai sem cores. FORCE_COLOR=1 mantém as cores quando outro
# programa captura a saída para exibir (o menu do demo.py).
COLORIDO = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"
ANSI = re.compile(r"\033\[[0-9;]*m")


def cor(codigo, texto):
    return f"\033[{codigo}m{texto}\033[0m" if COLORIDO else texto


def titulo(texto):
    print(cor("1;36", texto))
    print(cor("2", "─" * len(texto)))


def ok(condicao, descricao):
    """Imprime [OK] ou [FALHA] com a descrição."""
    marca = cor("1;32", "[OK]") if condicao else cor("1;31", "[FALHA]")
    print(f"{marca} {descricao}")


def visivel(texto):
    """Largura na tela: os códigos de cor não ocupam colunas."""
    return len(ANSI.sub("", texto))


def alinhar(texto, alinhamento, largura):
    """Como f'{texto:<largura}', mas contando só os caracteres visíveis ('<', '>' ou '^')."""
    folga = largura - visivel(texto)
    if alinhamento == ">":
        return " " * folga + texto
    if alinhamento == "^":
        return " " * (folga // 2) + texto + " " * (folga - folga // 2)
    return texto + " " * folga


def tabela(cabecalho, linhas, alinhamento=None):
    """Tabela com colunas alinhadas; alinhamento tem '<', '>' ou '^' por coluna (padrão: só a 1ª à esquerda)."""
    linhas = [[str(celula) for celula in linha] for linha in linhas]
    larguras = [max(visivel(str(celula)) for celula in coluna) for coluna in zip(cabecalho, *linhas)]
    alinhamento = alinhamento or "<" + ">" * (len(cabecalho) - 1)

    def formatar(linha):
        return "  ".join(alinhar(celula, a, w) for celula, a, w in zip(linha, alinhamento, larguras)).rstrip()

    print(cor("1", formatar([str(c) for c in cabecalho])))
    print("  ".join("─" * w for w in larguras))
    for linha in linhas:
        print(formatar(linha))


def compacta(lista):
    """Lista sem vírgulas, para caber no terminal: [3, 1, 2] -> [3 1 2]."""
    return "[" + " ".join(str(x) for x in lista) + "]"


def milhar(n):
    """Separador de milhar brasileiro: 1234567 -> 1.234.567."""
    return f"{n:,}".replace(",", ".")


def decimal(x, casas=1):
    """Número com vírgula decimal e ponto de milhar: 1024.5 -> 1.024,5."""
    return f"{x:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")


SIMBOLOS = {"chamada": ("36", "→"), "base": ("33", "■"), "retorno": ("32", "←")}


def recuo(nivel):
    """Guias verticais, uma por nível da pilha de recursão (a chamada inicial é o nível 1)."""
    return cor("2", "│ " * (nivel - 1))


def imprimir_rastro(evento, nivel, texto):
    """Callback de rastro: chamada (→), caso base (■) e retorno (←), recuados pelo nível da recursão."""
    codigo, simbolo = SIMBOLOS[evento]
    print(f"{recuo(nivel)}{cor(codigo, simbolo)} {texto}")
