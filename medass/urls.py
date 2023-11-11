from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'medass'

urlpatterns = [
    path('', views.medass_index, name='index'),
    path('<str:username>', views.medass_inquiry, name='inquiry')
]