"""
Views do aplicativo lists.
"""
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    """
    Página inicial.
    :return:
    """
    return render(request, 'home.html')


def view_list(request):
    """
    Visualizar lista.
    :return:
    """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    """
    Nova lista.
    :param request:
    :return:
    """
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')
