"""
Views do aplicativo lists.
"""
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


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
    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
            return render(request, 'list.html', {"list": list_, "error": error})
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """
    Nova lista.
    :param request:
    :return:
    """
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(list_)
