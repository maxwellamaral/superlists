"""
Testes de unidade do aplicativo lists.
"""
from django.test import TestCase


class SmokeTest(TestCase):
    """Teste de fumaça."""

    def test_bad_maths(self):
        """
        Teste: 1 + 1 = 2
        :return:
        """
        self.assertEqual(1 + 1, 3)
