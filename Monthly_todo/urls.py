from django.urls import path
from . import views

urlpatterns = [
    path('monthly/', views.index, name='monthly_index'),
    path('monthly/list/create/', views.list_create, name='monthly_list_create'),
    path('monthly/list/<int:list_id>/delete/', views.list_delete, name='monthly_list_delete'),
    path('monthly/list/<int:list_id>/task/add/', views.task_add, name='monthly_task_add'),
    path('monthly/task/<int:task_id>/delete/', views.task_delete, name='monthly_task_delete'),
    path('monthly/task/<int:task_id>/toggle/', views.task_toggle, name='monthly_task_toggle'),
]