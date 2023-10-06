from django.contrib import admin
from django.urls import path
from .views import index, registerCustomer, indexWithError, downloadData, downloadDataToday


urlpatterns = [
    path('', index, name='index'),
    path('', indexWithError, name='indexWithError'),
    path('output/', registerCustomer, name='register_customer'),
    path('export/', downloadData, name='down'),
    path('export-today/', downloadDataToday, name='down-today'),
]
