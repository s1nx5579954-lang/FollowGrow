from django.urls import path
from . import views

urlpatterns = [
    path('goalshare/', views.timeline, name='goalshare_timeline'),
    path('goalshare/reflection/create/', views.reflection_create, name='goalshare_reflection_create'),
    path('goalshare/search/', views.user_search, name='goalshare_user_search'),
    path('goalshare/follow/<int:user_id>/', views.follow_toggle, name='goalshare_follow_toggle'),
]