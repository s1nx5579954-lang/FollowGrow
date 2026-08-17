from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),                          
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('oneday/', include('OneDay_todo.urls')),                
    path('monthly/', include('Monthly_todo.urls')),
    path('', include('GoalShare.urls')),          
]