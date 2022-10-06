"""
Views do aplicativo lists.
"""
from django.shortcuts import render


def home_page(request):
    """
    Página inicial.
    :return:
    """
    return render(request, 'home.html')
