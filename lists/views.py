"""
Views do aplicativo lists.
"""
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    """
    Página inicial.
    :return:
    """
    return render(request, 'home.html')


def view_list(request, list_id):
    """
    Visualizar lista.
    :return:
    """
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    """
    Nova lista.
    :param request:
    :return:
    """
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
