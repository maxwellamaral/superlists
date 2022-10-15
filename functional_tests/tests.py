"""
Testes funcionais do Django.
"""
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from lists.models import Item, List

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    """Teste de novo visitante."""

    def setUp(self):
        """
        Configurações iniciais do caso de teste
        :return:
        """
        # * Edith tem um novo navegador
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """
        Finalização do caso de teste
        :return:
        """
        # * Edith fecha o navegador
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """
        Verifica se uma linha está na tabela de lista
        :param row_text:
        :return:
        """
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        """
        Espera pela lista de dados antes de realizar o teste
        :param row_text:
        :return:
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as exception:
                if time.time() - start_time > MAX_WAIT:
                    raise exception
                time.sleep(0.5)

    def test_layout_and_styling(self):
        """
        Teste: Testa layout e estilização
        :return:
        """
        # Edith acessa a página inicial
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Ela percebe que a caixa de entrada está elegantemente centralizada
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    def test_can_start_a_list_for_one_user(self):
        """
        Teste: Edith pode iniciar uma lista e recuperá-la mais tarde
        :return:
        """
        # Edith ouviu falar de uma nova aplicação online interessante para lista de tarefas. Ela decide
        # verificar sua homepage.
        self.browser.get(self.live_server_url)

        # Ela percebe que o título da página e o cabeçalho mencionam listas de tarefas (to-do)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente.
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Ela digita "Buy peacock feathers" (Comprar penas de pavão) em uma caixa de texto (o hobby
        # de Edith é fazer iscas # para pesca com fly).
        inputbox.send_keys('Buy peacock feathers')

        # Quando ela tecla enter, a página é atualizada, e agora a página lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas.
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar outro item.
        # Ela insere "Use peacock feathers to make a fly" (Usar penas de pavão para fazer
        # um fly - Edith é bem metódica).
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # A página é atualizada novamente e agora mostra os dois itens em sua lista.
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Satisfeita, ela volta a dormir.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """
        Teste: Vários usuários podem iniciar listas em URLs diferentes
        :return:
        """
        # Edith inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Ela percebe que sua lista tem um URL único
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Agora um novo usuário, Francis, chega ao site.

        # * Usamos uma nova sessão de navegador para garantir que nenhuma informação de Edith
        # * está vindo de cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis acessa a página inicial. Não há sinal de lista de Edith.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis inicia uma nova lista inserindo um novo item. Ele é menos interessante que
        # Edith...
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis obtém seu próprio URL exclusivo
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Novamente, não há nenhum sinal da lista de Edith
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfeitos, ambos voltam a dormir


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
