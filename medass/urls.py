from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'medass'

urlpatterns = [
    path('', views.medass, name='medass'),
]