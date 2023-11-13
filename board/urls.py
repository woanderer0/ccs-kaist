from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.board_index, name='index'),
    path('delete/<int:id>', views.board_delete, name='delete')
]