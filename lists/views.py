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
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})


def view_list(request):
    """
    Visualizar lista.
    :return:
    """
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
