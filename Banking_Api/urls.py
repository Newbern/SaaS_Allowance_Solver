from django.urls import path
from . import views

urlpatterns = [
    path('get_link_token/', views.get_link_token, name='get_link_token'),
    path('cuz/', views.cuz, name='cuz'),
    path('exchange_public_token/', views.exchange_public_token, name='exchange_public_token'),
]