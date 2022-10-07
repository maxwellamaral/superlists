"""
Testes de unidade do aplicativo lists.
"""
from django.test import TestCase


class HomePageTest(TestCase):
    """Teste de página inicial."""

    def test_home_page_returns_correct_html(self):
        """
        Teste: a página inicial retorna o HTML correto
        :return:
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
