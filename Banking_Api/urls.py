from django.urls import path
from Banking_Api import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('create-link-token/', views.create_link_token, name='create_link_token'),
    path('exchange-public-token/', views.exchange_public_token, name='exchange_public_token'),
]