from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('todo_list/', views.todo_list, name='todo_list'),
    path('AddTask/',views.addTask,name='add'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('update/<int:id>/', views.editTask, name='edit_task')
]
