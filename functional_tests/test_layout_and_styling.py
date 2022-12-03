"""
Testes funcionais do Django.
"""

from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest

MAX_WAIT = 10


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        """
        Teste: Testa layout e estilização
        :return:
        """
        # Edith acessa a página inicial
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Ela percebe que a caixa de entrada está elegantemente centralizada
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
