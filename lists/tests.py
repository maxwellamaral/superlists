"""
Testes de unidade do aplicativo lists.
"""
from django.http import HttpRequest
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

    def test_home_page_returns_correct_html(self):
        """
        Teste: a página inicial retorna o HTML correto
        :return:
        """
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
