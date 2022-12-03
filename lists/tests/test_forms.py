from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class ItemFormTest(TestCase):
    """
    Teste: o formulário renderiza o campo de texto do item
    """

    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        Teste: o formulário de entrada de item tem um marcador de posição e classes CSS
        :return:
        """
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        Teste: a validação do formulário para itens em branco
        :return:
        """
        form = ItemForm(data={'text': '', 'name': 'Max'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
