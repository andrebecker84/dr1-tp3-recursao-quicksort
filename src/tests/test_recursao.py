"""Testes das funções recursivas e da memoização (Exercícios 1 a 8).

    cd src && python3 -m unittest discover -s tests -t . -v
"""
import math
import os
import random
import tempfile
import unittest
from math import comb

from algoritmos.aritmetica import mult, mult_acumulando, power, power_linear
from algoritmos.combinacoes import teams
from algoritmos.diretorios import arquivos_por_nivel, percorrer
from algoritmos.fatoracao import factor
from algoritmos.metricas import medir
from algoritmos.mochila import contar_combinacoes, knapsack, knapsack_memo
from dados import criar_arvore
from verificacao import contar_com_os_walk, fatoracao_correta, subconjuntos_que_somam, times_de_referencia


class TestMult(unittest.TestCase):

    def test_resultado_igual_ao_produto(self):
        for x in range(-5, 25):
            for y in range(25):
                self.assertEqual(mult(x, y), x * y)
                self.assertEqual(mult_acumulando(x, y), x * y)

    def test_chamadas_somas_e_profundidade(self):
        _, metricas = medir(mult, 7, 40)
        self.assertEqual((metricas.chamadas, metricas.somas, metricas.profundidade), (41, 40, 41))

    def test_soma_no_retorno(self):
        eventos = []
        mult(5, 2, rastro=lambda evento, nivel, texto: eventos.append(evento))
        self.assertEqual(eventos, ["chamada", "chamada", "chamada", "base", "retorno", "retorno"])

    def test_y_negativo_recusado(self):
        with self.assertRaises(ValueError):
            mult(3, -1)


class TestFactor(unittest.TestCase):

    def test_fatoracao_correta(self):
        for x in range(-500, 5_001):
            self.assertTrue(fatoracao_correta(x, factor(x)), x)

    def test_casos_especiais(self):
        self.assertEqual([factor(0), factor(1), factor(-1), factor(-12)], [[0], [], [-1], [-1, 2, 2, 3]])

    def test_primo_testa_ate_a_raiz(self):
        fatores, metricas = medir(factor, 1_000_003)
        self.assertEqual((fatores, metricas.divisoes), ([1_000_003], 999))

    def test_lowest_invalido(self):
        with self.assertRaises(ValueError):
            factor(10, 1)


class TestPower(unittest.TestCase):

    def test_igual_ao_operador(self):
        for x in (-3, -2, -1, 0, 1, 2, 3, 0.5, 2.5):
            for y in range(-10, 33):
                if not (x == 0 and y < 0):
                    self.assertTrue(math.isclose(power(x, y), x ** y), (x, y))

    def test_casos_base(self):
        self.assertEqual((power(9, 0), power(9, 1), power(2, -3)), (1, 9, 0.125))

    def test_multiplicacoes_logaritmicas(self):
        for y in range(1, 3_000):
            self.assertLessEqual(medir(power, 3, y)[1].multiplicacoes, 2 * math.floor(math.log2(y)))
        self.assertEqual(medir(power_linear, 3, 500)[1].multiplicacoes, 499)

    def test_zero_com_expoente_negativo(self):
        with self.assertRaises(ZeroDivisionError):
            power(0, -2)


class TestDiretorios(unittest.TestCase):

    def test_mesmos_totais_do_os_walk(self):
        with tempfile.TemporaryDirectory() as raiz:
            criar_arvore(raiz)
            itens = percorrer(raiz)
            arquivos = sum(not item.diretorio for item in itens)
            diretorios = sum(item.diretorio for item in itens)
            self.assertEqual((arquivos, diretorios), contar_com_os_walk(raiz))

    def test_niveis_e_pre_ordem(self):
        with tempfile.TemporaryDirectory() as raiz:
            criar_arvore(raiz)
            itens, metricas = medir(percorrer, raiz)
            self.assertEqual(arquivos_por_nivel(itens)[4], ["fev.csv", "jan.csv", "jan.csv"])
            self.assertEqual((metricas.chamadas, metricas.profundidade), (10, 4))
            for anterior, atual in zip(itens, itens[1:]):
                self.assertLessEqual(atual.nivel, anterior.nivel + 1)
                if atual.nivel == anterior.nivel + 1:
                    self.assertTrue(anterior.diretorio)

    def test_nao_usa_travessia_pronta(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "algoritmos", "diretorios.py"), encoding="utf-8") as f:
            codigo = f.read().split('"""', 2)[2]
        self.assertNotIn("os.walk", codigo)
        self.assertNotIn("rglob", codigo)
        self.assertNotIn("glob(", codigo)


class TestTeams(unittest.TestCase):

    def test_igual_ao_itertools(self):
        for n in range(11):
            for k in range(n + 2):
                self.assertEqual(teams("ABCDEFGHIJ"[:n], k), times_de_referencia("ABCDEFGHIJ"[:n], k))

    def test_sem_repeticoes(self):
        times = teams("ABCDEFGHIJKLMN", 7)
        self.assertEqual(len(times), comb(14, 7))
        self.assertEqual(len(set(times)), len(times))

    def test_bordas(self):
        self.assertEqual((teams("ABC", 0), teams("ABC", 4), teams("ABCA", 2)), ([""], [], ["AB", "AC", "BC"]))


class TestKnapsack(unittest.TestCase):

    def test_exemplo_do_livro(self):
        self.assertEqual(knapsack(20, [11, 8, 7, 6, 5], 0), [[8, 7, 5]])

    def test_igual_a_forca_bruta(self):
        gerador = random.Random(7)
        for _ in range(150):
            pesos = [gerador.randint(1, 12) for _ in range(gerador.randint(0, 11))]
            alvo = gerador.randint(0, 35)
            self.assertEqual(sorted(sorted(c) for c in knapsack(alvo, pesos)), subconjuntos_que_somam(alvo, pesos))

    def test_explosao_de_chamadas(self):
        for n in range(1, 15):
            pesos = list(range(1, n + 1))
            self.assertEqual(medir(knapsack, sum(pesos) + 1, pesos)[1].chamadas, 2 ** (n + 1) - 1)

    def test_pesos_invalidos(self):
        with self.assertRaises(ValueError):
            knapsack(5, [2, -1])


class TestMemoizacao(unittest.TestCase):

    def test_mesmo_resultado_com_menos_chamadas(self):
        pesos = list(range(1, 19))
        alvo = sum(pesos) // 2
        pura, m_pura = medir(knapsack, alvo, pesos)
        memo, m_memo = medir(knapsack_memo, alvo, pesos)
        self.assertEqual(sorted(map(sorted, pura)), sorted(map(sorted, memo)))
        self.assertLess(m_memo.chamadas * 100, m_pura.chamadas)
        self.assertLessEqual(m_memo.chamadas, 2 * len(pesos) * (alvo + 1) + 1)

    def test_contagem(self):
        gerador = random.Random(11)
        for _ in range(100):
            pesos = [gerador.randint(1, 9) for _ in range(gerador.randint(0, 12))]
            alvo = gerador.randint(0, 30)
            self.assertEqual(contar_combinacoes(alvo, pesos), len(knapsack(alvo, pesos)))

    def test_escala_inviavel_sem_memo(self):
        pesos = list(range(1, 101))
        memo = {}
        quantidade, metricas = medir(contar_combinacoes, 2_525, pesos, 0, memo)
        self.assertEqual(quantidade, 1_731_024_005_948_725_016_633_786_324)
        self.assertLessEqual(len(memo), len(pesos) * 2_526)


if __name__ == "__main__":
    unittest.main()
