from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrance, name='entrance'),
    path('signup/', views.signup, name='signup'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
]