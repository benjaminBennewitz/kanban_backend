from django.contrib import admin
from django.urls import path

from ticketeer import views
from ticketeer.views import LoginView, RegisterView

# URL patterns for the Ticketeer application
# This configuration routes URLs to views.

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Login endpoint
    path('login/', views.LoginView.as_view(), name='login'),

    # Registration endpoint
    path('register/', views.RegisterView.as_view(), name='register'),

    # Endpoint for listing and creating tasks
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),

    # Endpoint for creating a task (alternative method)
    path('tasks/create/', views.create_task, name='create'),

    # Endpoint for retrieving, updating, and deleting a specific task by ID
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),

    # Endpoint for updating the status of a specific task by ID
    path('tasks/<int:pk>/status/', views.TaskStatusUpdateAPIView.as_view(), name='task-status-update'),
]