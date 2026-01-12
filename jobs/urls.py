from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'jobs'   # ✅ IMPORTANT (namespacing)

urlpatterns = [
    # Home and static pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Password reset - FIXED
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Job listings and details
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('jobs/<int:job_id>/save/', views.save_job, name='save_job'),
    path('application-success/', views.application_success, name='application_success'),

    # Job Seeker Dashboard
    path('seeker/dashboard/', views.seeker_dashboard, name='seeker_dashboard'),
    path('seeker/profile/', views.seeker_profile, name='seeker_profile'),

    # Employer Dashboard
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/profile/', views.employer_profile, name='employer_profile'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('employer/edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('employer/delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('employer/applications/<int:job_id>/', views.view_applications, name='view_applications'),
    path(
        'employer/application/<int:application_id>/update-status/',
        views.update_application_status,
        name='update_application_status'
    ),
]