"""
Testes de unidade do aplicativo lists.
"""
from django.test import TestCase

from lists.models import Item, List


class ListViewTest(TestCase):
    """Teste de visualização de lista."""

    def test_displays_all_items(self):
        """
        Teste: exibe todos os itens
        :return:
        """
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

    def test_uses_list_template(self):
        """
        Teste: usa o modelo de lista
        :return:
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        """
        Teste: exibe apenas itens para essa lista
        :return:
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='outro item 1', list=other_list)
        Item.objects.create(text='outro item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'outro item 1')
        self.assertNotContains(response, 'outro item 2')
