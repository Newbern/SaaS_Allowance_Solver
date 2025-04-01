from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-allowance/', views.create, name='create'),
    path('show-allowance/', views.show, name='show'),
    path('chart_data/', views.chart_data, name='chart_data'),
    path('history/', views.history, name='history'),
    path('chart_history_data/', views.chart_history_data, name='chart_history_data'),
    path('settings/', views.settings, name='settings')
]