"""
Arquivo de modelo para o aplicativo lists.
"""
from django.db import models


class Item(models.Model):
    """
    Modelo de item.
    """
    text = models.TextField(default='')
