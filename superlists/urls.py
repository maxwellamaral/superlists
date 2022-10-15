"""
Superlists URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from lists import views as lists_views
from lists import urls as lists_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lists_views.home_page, name='home'),
    path('lists/', include(lists_urls)),
]
