from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.list, name='data_list'),
    path('', views.main, name='main')
]