"""
Testes de unidade do aplicativo lists.
"""
from django.core.exceptions import ValidationError
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


class NewListTest(TestCase):
    """Teste de nova lista."""

    def test_can_save_a_post_request(self):
        """
        Teste: pode salvar uma requisição POST
        :return:
        """
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


class ItemModelsTest(TestCase):
    """Teste de modelo de item."""

    def test_cannot_save_empty_list_items(self):
        """
        Teste: não pode salvar itens de lista vazios
        :return:
        """
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()  # Força a validação em banco de dados sqlite.

    def test_duplicate_items_are_invalid(self):
        """
        Teste: itens duplicados são inválidos
        :return:
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_the_same_item_to_different_lists(self):
        """
        Teste: pode salvar o mesmo item em listas diferentes
        :return:
        """
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # Não deve gerar erro

    def test_list_ordering(self):
        """
        Teste: ordenação de lista
        :return:
        """
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        """
        Teste: representação de string
        :return:
        """
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

    def test_default_text(self):
        """
        Teste: texto padrão
        :return:
        """
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        """
        Teste: o item está relacionado à lista
        :return:
        """
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        """
        Teste: obter URL absoluta
        :return:
        """
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
