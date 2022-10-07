"""
Testes funcionais do Django.
"""
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
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
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
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

        # Edith se pergunta se o site lembrará de sua lista. Então ela nota que o site gerou um URL
        # único para ela - há um pequeno texto explicativo para isso.
        self.fail('Finish the test!')

        # Ela acessa esse URL - sua lista de tarefas continua lá.

        # Satisfeita, ela volta a dormir.
