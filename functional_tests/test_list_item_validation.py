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

        # A página inicial é atualizada e agora mostra uma mensagem de erro informando
        # que itens de lista não podem ser vazios.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You can't have an empty list item"
        ))

        # Ela tenta novamente com um texto para o item, o que agora funciona.
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # De forma perversa, ela agora decide submeter um segundo item vazio na lista.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Ela recebe uma mensagem semelhante na página da lista.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You can't have an empty list item"
        ))

        # E ela pode corrigir isso preenchendo o item com algum texto.
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2:')
        self.wait_for_row_in_list_table('3: Make tea')
