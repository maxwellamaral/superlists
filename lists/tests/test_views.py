"""
Testes de unidade do aplicativo lists.
"""
from unittest import skip

from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
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

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """
        Teste: erros de validação são enviados de volta ao modelo da página inicial
        :return:
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        """
        Teste: itens de lista inválidos não são salvos
        :return:
        """
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_passes_correct_list_to_template(self):
        """
        Teste: passa a lista correta para o modelo
        :return:
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        Teste: pode salvar uma solicitação POST para uma lista existente
        :return:
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """
        Teste: POST redireciona para a visualização da lista
        :return:
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        """
        Teste: erros de validação terminam na página de listas
        :return:
        """
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_display_item_form(self):
        """
        Teste: exibe o formulário de item
        :return:
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        """
        Post: entrada inválida
        :return:
        """
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        """
        Teste: para entrada inválida, nada é salvo no banco de dados
        :return:
        """
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        """
        Teste: para entrada inválida, renderiza o modelo de lista
        :return:
        """
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        """
        Teste: para entrada inválida, passa o formulário para o modelo
        :return:
        """
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        """
        Teste: erros de validação de itens duplicados terminam na página de listas
        :return:
        """
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )

        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class HomePageTest(TestCase):
    """Teste da página inicial."""

    def test_uses_home_template(self):
        """
        Teste: usa o modelo da página inicial
        :return:
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        """
        Teste: a página inicial usa o formulário de itens
        :return:
        """
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):
    """Teste de nova lista."""

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """
        Teste: erros de validação são enviados de volta ao modelo da página inicial
        :return:
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_for_invalid_input_renders_home_template(self):
        """
        Teste: para entrada inválida, renderiza o modelo da página inicial
        :return:
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        """
        Teste: para entrada inválida, erros de validação são mostrados na página inicial
        :return:
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        """
        Teste: para entrada inválida, passa o formulário para o modelo
        :return:
        """
        response = self.client.post('/lists/new', data={'text': ''})

        # ! assertIsInstance é usado para verificar se o objeto é uma instância de uma classe
        self.assertIsInstance(response.context['form'], ItemForm)
