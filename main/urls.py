from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-allowance/', views.create, name='create'),
    path('settings/', views.settings, name='settings'),
]