from django.contrib import admin
from .models import UserProfile, Job, Application, SavedJob, Contact


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'location', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'company_name', 'phone']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'category', 'job_type', 'location', 'is_active', 'posted_date']
    list_filter = ['category', 'job_type', 'is_active', 'posted_date']
    search_fields = ['title', 'company_name', 'location', 'description']
    date_hierarchy = 'posted_date'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_date']
    list_filter = ['status', 'applied_date']
    search_fields = ['applicant__username', 'job__title', 'contact_email']
    date_hierarchy = 'applied_date'


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'saved_date']
    list_filter = ['saved_date']
    search_fields = ['user__username', 'job__title']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_resolved']
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'