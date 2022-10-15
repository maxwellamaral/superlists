"""
Arquivo de modelo para o aplicativo lists.
"""
from django.db import models


class List(models.Model):
    """
    Modelo de lista.
    """
    pass

class Item(models.Model):
    """
    Modelo de item.
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, null=True, on_delete=models.CASCADE)


