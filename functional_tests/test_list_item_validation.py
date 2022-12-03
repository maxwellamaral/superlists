"""
Testes funcionais do Django.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        """
        Teste: Não é possível adicionar itens vazios na lista
        :return:
        """
        # Edith acessa a página inicial e acidentalmente tenta enviar um item vazio na lista.
        # Ela tecla Enter na caixa de entrada vazia
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # O navegador intercepta a requisição e não carrega a página da lista
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        # Ela começa a digitar algum texto para o novo item e o erro desaparece
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))

        # Ela pode submeter um item com sucesso
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # De forma perversa, ela agora decide submeter um segundo item vazio na lista.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Novamente, o navegador não vai aceitar isso.
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        # E ela pode corrigir isso preenchendo o item com algum texto.
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        """
        Teste: Não é possível adicionar itens duplicados
        :return:
        """
        # Edith acessa a página inicial e começa uma nova lista
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # Ela acidentalmente tenta inserir um item duplicado
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Ela vê uma mensagem de erro útil
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You've already got this in your list"
        ))
