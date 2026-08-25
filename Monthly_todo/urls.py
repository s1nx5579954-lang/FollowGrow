from django.urls import path
from . import views

urlpatterns = [
    path('monthly/', views.index, name='monthly_index'),
    path('monthly/list/create/', views.list_create, name='monthly_list_create'),
    path('monthly/list/<int:list_id>/delete/', views.list_delete, name='monthly_list_delete'),
]