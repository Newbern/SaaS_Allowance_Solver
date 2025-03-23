from django.urls import path
from . import views

urlpatterns = [
    path('get_link_token/', views.get_link_token, name='get_link_token'),
    path('cuz/', views.cuz, name='cuz'),
]