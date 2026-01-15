from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.utils import timezone

from jobs.models import Job, Application, UserProfile, SavedJob, Contact


# Admin check decorator
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access denied. Admin only.")
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# =========================
# Dashboard & Overview
# =========================

@login_required
@admin_required
def admin_dashboard(request):
    """Main admin dashboard with statistics"""
    
    # Get date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Overall statistics
    stats = {
        'total_users': User.objects.count(),
        'total_seekers': UserProfile.objects.filter(user_type='seeker').count(),
        'total_employers': UserProfile.objects.filter(user_type='employer').count(),
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'total_contacts': Contact.objects.count(),
        'unresolved_contacts': Contact.objects.filter(is_resolved=False).count(),
    }
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_jobs = Job.objects.order_by('-posted_date')[:5]
    recent_applications = Application.objects.order_by('-applied_date')[:5]
    recent_contacts = Contact.objects.order_by('-created_at')[:5]
    
    # Growth statistics
    new_users_this_week = User.objects.filter(date_joined__gte=week_ago).count()
    new_jobs_this_week = Job.objects.filter(posted_date__gte=week_ago).count()
    new_applications_this_week = Application.objects.filter(applied_date__gte=week_ago).count()
    
    context = {
        'stats': stats,
        'recent_users': recent_users,
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
        'recent_contacts': recent_contacts,
        'new_users_this_week': new_users_this_week,
        'new_jobs_this_week': new_jobs_this_week,
        'new_applications_this_week': new_applications_this_week,
    }
    
    return render(request, 'dashboard.html', context)


# =========================
# User Management
# =========================

@login_required
@admin_required
def manage_users(request):
    """Manage all users"""
    
    search_query = request.GET.get('search', '')
    user_type = request.GET.get('type', '')
    
    users = User.objects.select_related('profile').all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if user_type:
        users = users.filter(profile__user_type=user_type)
    
    users = users.order_by('-date_joined')
    
    paginator = Paginator(users, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'user_type': user_type,
    }
    
    return render(request, 'manage_users.html', context)


@login_required
@admin_required
def user_detail(request, user_id):
    """View and edit user details"""
    
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    
    # Get user's activity
    if profile.user_type == 'seeker':
        applications = Application.objects.filter(applicant=user)
        saved_jobs = SavedJob.objects.filter(user=user)
        posted_jobs = None
    else:
        applications = None
        saved_jobs = None
        posted_jobs = Job.objects.filter(employer=user)
    
    context = {
        'user': user,
        'profile': profile,
        'applications': applications,
        'saved_jobs': saved_jobs,
        'posted_jobs': posted_jobs,
    }
    
    return render(request, 'user_detail.html', context)


@login_required
@admin_required
def delete_user(request, user_id):
    """Delete a user"""
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully')
        return redirect('admin_panel:manage_users')
    
    return render(request, 'delete_user_confirm.html', {'user': user})


@login_required
@admin_required
def toggle_user_status(request, user_id):
    """Activate/Deactivate user"""
    
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.username} {status} successfully')
    
    return redirect('admin_panel:user_detail', user_id=user_id)


# =========================
# Job Management
# =========================

@login_required
@admin_required
def manage_jobs(request):
    """Manage all jobs"""
    
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    
    jobs = Job.objects.select_related('employer').all()
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category:
        jobs = jobs.filter(category=category)
    
    if status == 'active':
        jobs = jobs.filter(is_active=True)
    elif status == 'inactive':
        jobs = jobs.filter(is_active=False)
    
    jobs = jobs.order_by('-posted_date')
    
    paginator = Paginator(jobs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'status': status,
        'job_categories': Job.CATEGORIES,
    }
    
    return render(request, 'manage_jobs.html', context)


@login_required
@admin_required
def job_detail(request, job_id):
    """View job details"""
    
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job)
    
    context = {
        'job': job,
        'applications': applications,
    }
    
    return render(request, 'job_detail.html', context)


@login_required
@admin_required
def delete_job(request, job_id):
    """Delete a job"""
    
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f'Job "{job_title}" deleted successfully')
        return redirect('admin_panel:manage_jobs')
    
    return render(request, 'delete_job_confirm.html', {'job': job})


@login_required
@admin_required
def toggle_job_status(request, job_id):
    """Activate/Deactivate job"""
    
    job = get_object_or_404(Job, id=job_id)
    job.is_active = not job.is_active
    job.save()
    
    status = 'activated' if job.is_active else 'deactivated'
    messages.success(request, f'Job "{job.title}" {status} successfully')
    
    return redirect('admin_panel:job_detail', job_id=job_id)


# =========================
# Application Management
# =========================

@login_required
@admin_required
def manage_applications(request):
    """Manage all applications"""
    
    search_query = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    applications = Application.objects.select_related('job', 'applicant').all()
    
    if search_query:
        applications = applications.filter(
            Q(job__title__icontains=search_query) |
            Q(applicant__username__icontains=search_query)
        )
    
    if status:
        applications = applications.filter(status=status)
    
    applications = applications.order_by('-applied_date')
    
    paginator = Paginator(applications, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status': status,
        'status_choices': Application.STATUS_CHOICES,
    }
    
    return render(request, 'manage_applications.html', context)


@login_required
@admin_required
def application_detail(request, application_id):
    """View application details"""
    
    application = get_object_or_404(Application, id=application_id)
    
    context = {
        'application': application,
    }
    
    return render(request, 'application_detail.html', context)


@login_required
@admin_required
def delete_application(request, application_id):
    """Delete an application"""
    
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Application deleted successfully')
        return redirect('admin_panel:manage_applications')
    
    return render(request, 'delete_application_confirm.html', {'application': application})


# =========================
# Contact Management
# =========================

@login_required
@admin_required
def manage_contacts(request):
    """Manage contact messages"""
    
    status = request.GET.get('status', '')
    
    contacts = Contact.objects.all()
    
    if status == 'resolved':
        contacts = contacts.filter(is_resolved=True)
    elif status == 'unresolved':
        contacts = contacts.filter(is_resolved=False)
    
    contacts = contacts.order_by('-created_at')
    
    paginator = Paginator(contacts, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'status': status,
    }
    
    return render(request, 'manage_contacts.html', context)


@login_required
@admin_required
def contact_detail(request, contact_id):
    """View contact message details"""
    
    contact = get_object_or_404(Contact, id=contact_id)
    
    context = {
        'contact': contact,
    }
    
    return render(request, 'contact_detail.html', context)


@login_required
@admin_required
def toggle_contact_status(request, contact_id):
    """Mark contact as resolved/unresolved"""
    
    contact = get_object_or_404(Contact, id=contact_id)
    contact.is_resolved = not contact.is_resolved
    contact.save()
    
    status = 'resolved' if contact.is_resolved else 'unresolved'
    messages.success(request, f'Contact marked as {status}')
    
    return redirect('admin_panel:contact_detail', contact_id=contact_id)


@login_required
@admin_required
def delete_contact(request, contact_id):
    """Delete a contact message"""
    
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact message deleted successfully')
        return redirect('admin_panel:manage_contacts')
    
    return render(request, 'delete_contact_confirm.html', {'contact': contact})


# =========================
# Analytics & Reports
# =========================

@login_required
@admin_required
def analytics(request):
    """Analytics and reports"""
    
    # User analytics
    total_users = User.objects.count()
    seekers = UserProfile.objects.filter(user_type='seeker').count()
    employers = UserProfile.objects.filter(user_type='employer').count()
    
    # Job analytics
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(is_active=True).count()
    jobs_by_category = Job.objects.values('category').annotate(count=Count('id'))
    
    # Application analytics
    total_applications = Application.objects.count()
    applications_by_status = Application.objects.values('status').annotate(count=Count('id'))
    
    # Monthly growth
    last_6_months = []
    for i in range(6):
        month_date = timezone.now() - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        
        users_count = User.objects.filter(date_joined__gte=month_start).count()
        jobs_count = Job.objects.filter(posted_date__gte=month_start).count()
        
        last_6_months.append({
            'month': month_start.strftime('%B %Y'),
            'users': users_count,
            'jobs': jobs_count,
        })
    
    last_6_months.reverse()
    
    context = {
        'total_users': total_users,
        'seekers': seekers,
        'employers': employers,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'jobs_by_category': jobs_by_category,
        'total_applications': total_applications,
        'applications_by_status': applications_by_status,
        'last_6_months': last_6_months,
    }
    
    return render(request, 'analytics.html', context)