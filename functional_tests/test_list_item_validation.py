"""
Testes funcionais do Django.
"""
from unittest import skip

from functional_tests.base import FunctionalTest

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_list_items(self):
        """
        Teste: Não é possível adicionar itens vazios na lista
        :return:
        """
        # Edith acessa a página inicial e acidentalmente tenta enviar um item vazio na lista.
        # Ela tecla Enter na caixa de entrada vazia
        # A página inicial é atualizada e agora mostra uma mensagem de erro informando
        # que itens de lista não podem ser vazios.
        # Ela tenta novamente com um texto para o item, o que agora funciona.
        # De forma perversa, ela agora decide submeter um segundo item vazio na lista.
        # Ela recebe uma mensagem semelhante na página da lista.
        # E ela pode corrigir isso preenchendo o item com algum texto.
        self.fail('Write me!')
