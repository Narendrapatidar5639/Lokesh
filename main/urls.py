# main/urls.py
from django.urls import path
from .views import register_api, login_api
from . import views

urlpatterns = [
    # GET
    path('projects/', views.projects_api, name='projects_api'),
    path('projects/<int:id>/', views.project_detail_api, name='project_detail_api'),
    path('categories/', views.categories_list, name='categories_list'),
    path('projects/<int:project_id>/feedback/', views.add_feedback_api, name='add_feedback_api'),

    # POST (Admin)
    path('projects/add/', views.add_project_api, name='add_project_api'),  # Admin add
    path('projects/<int:pk>/delete/', views.delete_project_api, name='delete_project_api'),  # Admin delete
    
    #login/signup
    path('register/', views.register_api),
    path('login/', views.login_api),
]
