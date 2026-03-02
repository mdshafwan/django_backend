# todo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Todo (Template views)
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('update/<int:pk>/', views.todo_update, name='todo_update'),
    path('delete/<int:pk>/', views.todo_delete, name='todo_delete'),

    # API
    path('api/todo/', views.TodoListCreateAPI.as_view(), name='api_todo'),
    path('api/todo/<int:pk>/', views.TodoDetailAPI.as_view(), name='api_todo_detail'),
]