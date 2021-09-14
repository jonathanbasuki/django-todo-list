from django.urls import path # import path method
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage # import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage classes // views.py
from django.contrib.auth.views import LogoutView # import django logout view // built-in view

urlpatterns = [
	path('login/', CustomLoginView.as_view(), name = 'login'),
	path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),
	path('register/', RegisterPage.as_view(), name = 'register'),

	path('', TaskList.as_view(), name = 'tasks'),
	path('task/<int:pk>/', TaskDetail.as_view(), name = 'task'),
	path('task-create/', TaskCreate.as_view(), name = 'task-create'),
	path('task-update/<int:pk>/', TaskUpdate.as_view(), name = 'task-update'),
	path('task-delete/<int:pk>/', TaskDelete.as_view(), name = 'task-delete'),
]