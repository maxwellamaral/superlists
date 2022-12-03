"""
Testes funcionais do Django.
"""

from django.test import LiveServerTestCase
from selenium import webdriver

from lists.models import Item, List

MAX_WAIT = 10


class ListViewTest(LiveServerTestCase):
    """
    Teste de visualização de lista
    """

    def setUp(self):
        """
        Configurações iniciais do caso de teste
        :return:
        """
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """
        Finalização do caso de teste
        :return:
        """
        self.browser.quit()

    def test_displays_all_list_items(self):
        """
        Teste: O item da lista é exibido em todas as páginas
        :return:
        """
        # Edith cria uma nova lista de tarefas
        list_ = List.objects.create()

        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        # Ela acessa a página inicial e vê que sua lista está lá
        response = self.client.get(f'/lists/{list_.id}/')
        # * Lida com respostas e bytes de seu conteúdo.
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
