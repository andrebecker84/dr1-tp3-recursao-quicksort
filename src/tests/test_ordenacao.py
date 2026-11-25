"""Testes da partição, do QuickSort e do QuickSelect (Exercícios 9 a 12).

    cd src && python3 -m unittest discover -s tests -t . -v
"""
import random
import sys
import unittest

from algoritmos.metricas import Metricas, medir
from algoritmos.ordenacao import mediana, particionar, quickselect, quicksort
from dados import ARRAY_DO_LIVRO, Cenario, lista_no_cenario

sys.setrecursionlimit(10_000)


def listas_aleatorias(quantidade, semente=3):
    gerador = random.Random(semente)
    return [[gerador.randint(0, gerador.choice((1, 4, 50, 1_000))) for _ in range(gerador.randint(0, 70))]
            for _ in range(quantidade)]


class TestParticao(unittest.TestCase):

    def test_exemplo_do_livro(self):
        lista = list(ARRAY_DO_LIVRO)
        pivo = particionar(lista, 0, len(lista) - 1, Metricas())
        self.assertEqual((pivo, lista), (3, [0, 1, 2, 3, 6, 5]))

    def test_lados_do_pivo(self):
        for lista in listas_aleatorias(1_500):
            if lista:
                pivo = particionar(lista, 0, len(lista) - 1, Metricas())
                self.assertTrue(all(x <= lista[pivo] for x in lista[:pivo]))
                self.assertTrue(all(x >= lista[pivo] for x in lista[pivo + 1:]))


class TestQuickSort(unittest.TestCase):

    def test_igual_ao_sorted(self):
        for lista in listas_aleatorias(2_000):
            self.assertEqual(quicksort(lista), sorted(lista))

    def test_entrada_intacta(self):
        lista = [5, 3, 9, 1]
        quicksort(lista)
        self.assertEqual(lista, [5, 3, 9, 1])

    def test_pior_caso_ordenada(self):
        for n in (2, 10, 500):
            _, metricas = medir(quicksort, list(range(n)))
            self.assertEqual((metricas.comparacoes, metricas.copias, metricas.profundidade), (n * (n + 1) // 2 - 2, 0, n))

    def test_copias_multiplas_de_tres(self):
        for cenario in Cenario:
            self.assertEqual(medir(quicksort, lista_no_cenario(300, cenario))[1].copias % 3, 0)

    def test_aleatoria_n_log_n(self):
        _, metricas = medir(quicksort, lista_no_cenario(4_096, Cenario.ALEATORIA))
        self.assertLess(metricas.comparacoes, 2 * 4_096 * 12)
        self.assertLess(metricas.profundidade, 4 * 12)


class TestQuickSelect(unittest.TestCase):

    def test_todos_os_indices(self):
        for lista in listas_aleatorias(400, semente=9):
            ordenada = sorted(lista)
            for k in range(len(lista)):
                self.assertEqual(quickselect(lista, k), ordenada[k])

    def test_mediana(self):
        self.assertEqual((mediana([9, 4, 7, 1, 8, 2, 6, 5, 3]), mediana([4, 1, 3, 2]), mediana([8])), (5, 2.5, 8))

    def test_menos_trabalho_que_ordenar(self):
        lista = lista_no_cenario(20_001, Cenario.ALEATORIA)
        selecao = medir(quickselect, lista, 10_000)[1]
        ordenacao = medir(quicksort, lista)[1]
        self.assertLess(selecao.comparacoes * 2, ordenacao.comparacoes)
        self.assertLess(selecao.chamadas, ordenacao.chamadas)

    def test_indice_invalido(self):
        for k in (-1, 3, 1.0):
            with self.assertRaises(IndexError):
                quickselect([1, 2, 3], k)


if __name__ == "__main__":
    unittest.main()
