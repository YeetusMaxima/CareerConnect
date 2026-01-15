from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='dashboard'),
    
    # User Management
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    
    # Job Management
    path('jobs/', views.manage_jobs, name='manage_jobs'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/toggle-status/', views.toggle_job_status, name='toggle_job_status'),
    
    # Application Management
    path('applications/', views.manage_applications, name='manage_applications'),
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),
    path('applications/<int:application_id>/delete/', views.delete_application, name='delete_application'),
    
    # Contact Management
    path('contacts/', views.manage_contacts, name='manage_contacts'),
    path('contacts/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:contact_id>/toggle-status/', views.toggle_contact_status, name='toggle_contact_status'),
    path('contacts/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
]