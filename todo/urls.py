from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create_list/', views.create_list, name='create_list'),
    path('home/', views.home, name='home'),
    path('home/<int:list_id>/', views.home, name='home'),
    path('home/<int:list_id>/edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('home/<int:list_id>/delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    # path('home/<int:list_id>/complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('home/delete/', views.delete_list, name='delete_list'),
    path('home/edit/<int:list_id>/', views.edit_list, name='edit_list'),
]
