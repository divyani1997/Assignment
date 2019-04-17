from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.index, name='index'),
    path('info', views.detail),
]