from django.urls import path
from . import views

urlpatterns = [
    path('monthly/', views.index, name='monthly_index'),
    path('monthly/list/create/', views.list_create, name='monthly_list_create'),
    path('monthly/list/<int:list_id>/delete/', views.list_delete, name='monthly_list_delete'),
    path('monthly/list/<int:list_id>/toggle/', views.list_toggle, name='monthly_list_toggle'),
    path('monthly/check-deadlines/', views.check_deadlines, name='monthly_check_deadlines'),
    path('monthly/list/bulk-delete-completed/', views.bulk_delete_completed, name='monthly_bulk_delete_completed'),
]