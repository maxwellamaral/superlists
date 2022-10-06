"""
Views do aplicativo lists.
"""
from django.http import HttpResponse


def home_page(request):
    """
    Página inicial.
    :return:
    """
    return HttpResponse('<html><title>To-Do lists</title></html>')
