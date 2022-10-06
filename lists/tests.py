"""
Testes de unidade do aplicativo lists.
"""
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """Teste de página inicial."""

    def test_root_url_resolves_to_home_page_view(self):
        """
        Teste: URL raiz resolve para a página inicial
        :return:
        """
        found = resolve('/')
        self.assertEqual(found.func, home_page)
