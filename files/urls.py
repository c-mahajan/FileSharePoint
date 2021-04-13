from django.http import request
from files.models import UserFile
from django.urls import path
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    path('', views.index, name='index'),
    path('myfiles/', views.myfiles, name='myfiles'),
    path('save/', views.save_file, name='save'),
    path('share_file/<int:file_id>/', views.share_file, name='share_file'),
    path('rename_file/<int:file_id>/', views.rename_file, name='rename_file'),
    path('move_to_trash/<int:file_id>/', views.move_to_trash, name='move_to_trash'),
    path('restore/<int:file_id>/', views.restore, name='restore'),
    path('shared_with_me/', views.shared_with_me, name='shared_with_me'),
    path('mytrash/', views.mytrash, name='mytrash'),
    path('permanent_delete/<int:file_id>', views.permanent_delete, name='permanent_delete'),
    path(f'user_files/user_<int:user_id>/<str:file>', views.serverFile, name='serverfile'),
]