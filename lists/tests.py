"""
Testes de unidade do aplicativo lists.
"""
from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):
    """Teste de página inicial."""

    def test_home_page_returns_correct_html(self):
        """
        Teste: a página inicial retorna o HTML correto
        :return:
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    class ListViewTest(TestCase):
        """Teste de visualização de lista."""

        def test_uses_list_template(self):
            """
            Teste: usa o modelo de lista
            :return:
            """
            response = self.client.get('/lists/the-only-list-in-the-world/')
            self.assertTemplateUsed(response, 'list.html')


class ListAndItemModelsTest(TestCase):
    """Teste de modelo de item."""

    def test_saving_and_retrieving_items(self):
        """
        Teste: salvando e recuperando listas e itens no modelo de dados
        :return:
        """
        # Criando uma lista
        list_ = List()
        list_.save()

        # Criando itens
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        # Carregando listas e itens que constam no banco de dados até agora e verificando se elas são as mesmas criadas
        # anteriormente. Neste caso, comparando um conjunto.
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        # Verificando se os itens salvos especificamente são os mesmos que foram criados anteriormente. Neste caso
        # comparando um item por vez (cada campo)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class NewListTest(TestCase):
    """Teste de nova lista."""

    def test_can_save_a_post_request(self):
        """
        Teste: pode salvar uma requisição POST
        :return:
        """
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """
        Teste: redireciona após POST
        :return:
        """
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        # * Vou substituir as duas linhas abaixo por uma linha só:
        # * self.assertEqual(response.status_code, 302)
        # * self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
