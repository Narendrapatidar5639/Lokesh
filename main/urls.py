from django.urls import path
from . import views
from .views import google_check  # Import the new view

urlpatterns = [
    # GET
    path('projects/', views.projects_api, name='projects_api'),
    path('projects/<int:id>/', views.project_detail_api, name='project_detail_api'),
    path('categories/', views.categories_list, name='categories_list'),
    path('projects/<int:project_id>/feedback/', views.add_feedback_api, name='add_feedback_api'),

    # ADMIN
    path('projects/add/', views.add_project_api, name='add_project_api'),
    path('projects/<int:pk>/delete/', views.delete_project_api, name='delete_project_api'),
    path('projects/<int:pk>/update/', views.update_project_api, name='update_project_api'),
    path('feedbacks/<int:pk>/delete/', views.delete_feedback_api, name='delete_feedback_api'),
    path('images/<int:pk>/delete/', views.delete_image_api, name='delete_image_api'),

    # AUTH
    path('register/', views.register_api),
    path('login/', views.login_api),
    
    path('google-check/', google_check, name='google-check'),
    path('reset-password/', views.reset_password_api, name='reset_password_api'),
]