"""
Testes funcionais do Django.
"""
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        """
        Configurações iniciais do caso de teste
        :return:
        """
        # * Edith tem um novo navegador
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f'http://{staging_server}'

    def tearDown(self):
        """
        Finalização do caso de teste
        :return:
        """
        # * Edith fecha o navegador
        self.browser.quit()

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

    def wait_for(self, fn):
        """
        Espera pela lista de dados antes de realizar o teste
        :param fn:
        :return:
        """
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as exception:
                if time.time() - start_time > MAX_WAIT:
                    raise exception
                time.sleep(0.5)

    def get_item_input_box(self):
        """
        Retorna o elemento input box
        :return:
        """
        return self.browser.find_element(By.ID, 'id_text')
