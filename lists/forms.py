from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.models.ModelForm):
    """
    Formulário de item.
    """

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        # ! Para personalizar o erro de formulário, você pode usar o atributo error_messages
        # ! Neste caso, quero personalizar o erro de validação de campo vazio ou campo requerido.
        # ! Quando um erro de formulário ocorre, o Django preenche uma lista de erros de formulário em forms.errors.
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        """
        Salva o formulário.
        :param for_list:
        :return:
        """
        self.instance.list = for_list
        return super().save()

class ExistingListItemForm(ItemForm):
    """
    Formulário de item existente.
    """

    def __init__(self, for_list, *args, **kwargs):
        """
        Inicializa o formulário.
        :param for_list:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        """
        Valida o formulário.
        :return:
        """
        try:
            self.instance.validate_unique()
        except forms.ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)