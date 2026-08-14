# OneDay_todo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='oneday_index'),
    path('list/create/', views.list_create, name='list_create'),
    path('list/<int:list_id>/delete/', views.list_delete, name='list_delete'), 
    path('list/<int:list_id>/task/add/', views.task_add, name='task_add'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:task_id>/toggle/', views.task_toggle, name='task_toggle'),
]