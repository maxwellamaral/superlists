"""
Views do aplicativo lists.
"""
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR


def home_page(request):
    """
    Página inicial.
    :return:
    """
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    """
    Visualizar lista.
    :return:
    """
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    """
    Nova lista.
    :param request:
    :return:
    """
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})