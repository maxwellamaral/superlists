"""
Arquivo de modelo para o aplicativo lists.
"""
from django.db import models
from django.urls import reverse


class List(models.Model):
    """
    Modelo de lista.
    """
    def get_absolute_url(self):
        """
        Obter URL absoluta.
        :return:
        """
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    """
    Modelo de item.
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, null=True, on_delete=models.CASCADE)


