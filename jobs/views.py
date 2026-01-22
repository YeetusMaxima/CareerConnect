from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from .models import Job, Application, SavedJob, UserProfile, Contact
from .forms import (
    UserRegistrationForm,
    JobSeekerProfileForm,
    EmployerProfileForm,
    JobPostForm,
    JobApplicationForm,
    JobSearchForm,
    ContactForm
)
# ✅ UPDATED: Import both recommendation functions
from .ml_recommender import get_job_recommendations, get_candidate_recommendations


# =========================
# Home & Static Pages
# =========================

def home(request):
    recent_jobs = Job.objects.filter(is_active=True).order_by('-posted_date')[:6]
    job_categories = Job.CATEGORIES
    
    recommended_jobs = []
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        if request.user.profile.user_type == 'seeker':
            try:
                recommended_jobs = get_job_recommendations(request.user, count=6)
            except Exception as e:
                print(f"Recommendation error: {e}")
                recommended_jobs = []
    
    return render(request, 'home.html', {
        'recent_jobs': recent_jobs,
        'job_categories': job_categories,
        'recommended_jobs': recommended_jobs,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us!')
            return redirect('jobs:contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


# =========================
# Authentication
# =========================

def register(request):
    if request.user.is_authenticated:
        return redirect('jobs:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            phone = form.cleaned_data.get('phone')
            
            UserProfile.objects.create(
                user=user, 
                user_type=user_type,
                phone=phone
            )
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('jobs:login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_panel:dashboard')
        return redirect('jobs:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            
            if user.is_superuser:
                messages.success(request, f'Welcome back, Admin {user.username}!')
                return redirect('admin_panel:dashboard')
            
            next_url = request.GET.get('next', 'jobs:home')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('jobs:home')


# =========================
# Jobs – Listing & Detail
# =========================

@login_required
def job_listings(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.filter(is_active=True)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        location = form.cleaned_data.get('location')
        category = form.cleaned_data.get('category')
        job_type = form.cleaned_data.get('job_type')
        min_salary = form.cleaned_data.get('min_salary')

        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(skills_required__icontains=keyword)
            )
        if location:
            jobs = jobs.filter(location__icontains=location)
        if category:
            jobs = jobs.filter(category=category)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if min_salary:
            jobs = jobs.filter(salary_min__gte=min_salary)

    sort_by = request.GET.get('sort', '-posted_date')
    if sort_by in ['-posted_date', 'salary_max', '-salary_max']:
        jobs = jobs.order_by(sort_by)

    paginator = Paginator(jobs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    recommended_jobs = []
    if request.user.profile.user_type == 'seeker':
        try:
            recommended_jobs = get_job_recommendations(request.user, count=6)
        except Exception as e:
            print(f"Recommendation error: {e}")
            recommended_jobs = []

    return render(request, 'job_listings.html', {
        'form': form,
        'page_obj': page_obj,
        'total_jobs': jobs.count(),
        'recommended_jobs': recommended_jobs,
    })


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    is_saved = False
    has_applied = False

    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
        has_applied = Application.objects.filter(applicant=request.user, job=job).exists()
    
    similar_jobs = []
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        if request.user.profile.user_type == 'seeker':
            try:
                similar_jobs = get_job_recommendations(request.user, count=4)
            except Exception as e:
                print(f"Recommendation error: {e}")
                similar_jobs = []

    return render(request, 'job_detail.html', {
        'job': job,
        'is_saved': is_saved,
        'has_applied': has_applied,
        'similar_jobs': similar_jobs,
    })


# =========================
# Job Application
# =========================

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    if request.user.profile.user_type != 'seeker':
        messages.error(request, 'Only job seekers can apply')
        return redirect('jobs:job_detail', job_id=job_id)

    if Application.objects.filter(applicant=request.user, job=job).exists():
        messages.warning(request, 'You have already applied')
        return redirect('jobs:job_detail', job_id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully')
            return redirect('jobs:application_success')
    else:
        form = JobApplicationForm(initial={
            'contact_email': request.user.email,
            'contact_phone': request.user.profile.phone
        })

    return render(request, 'apply_job.html', {'form': form, 'job': job})


@login_required
def application_success(request):
    return render(request, 'application_success.html')


@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.profile.user_type != 'seeker':
        messages.error(request, 'Only job seekers can save jobs')
        return redirect('jobs:job_detail', job_id=job_id)

    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        saved.delete()
        messages.success(request, 'Job removed from saved list')
    else:
        messages.success(request, 'Job saved successfully')

    return redirect('jobs:job_detail', job_id=job_id)


# =========================
# Seeker Area
# =========================

@login_required
def seeker_dashboard(request):
    if request.user.profile.user_type != 'seeker':
        return HttpResponseForbidden("Access denied")
    
    recommended_jobs = []
    try:
        recommended_jobs = get_job_recommendations(request.user, count=6)
    except Exception as e:
        print(f"Recommendation error: {e}")
        recommended_jobs = []

    return render(request, 'seeker_dashboard.html', {
        'applications': Application.objects.filter(applicant=request.user),
        'saved_jobs': SavedJob.objects.filter(user=request.user),
        'recommended_jobs': recommended_jobs,
    })


@login_required
def seeker_profile(request):
    if request.user.profile.user_type != 'seeker':
        return HttpResponseForbidden("Access denied")

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=request.user.profile)

        # DEBUG: print incoming files
        print("FILES coming from form:", request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('jobs:seeker_dashboard')
        else:
            print("Form errors:", form.errors)

    else:
        form = JobSeekerProfileForm(instance=request.user.profile)

    return render(request, 'seeker_profile.html', {'form': form})


# =========================
# Employer Area
# =========================

@login_required
def employer_dashboard(request):
    if request.user.profile.user_type != 'employer':
        return HttpResponseForbidden("Access denied")
    
    # ✅ ADDED: Get recommended candidates for employer's jobs
    employer_jobs = Job.objects.filter(employer=request.user, is_active=True)
    recommended_candidates = []
    
    if employer_jobs.exists():
        latest_job = employer_jobs.first()
        try:
            recommended_candidates = get_candidate_recommendations(latest_job, count=6)
        except Exception as e:
            print(f"Candidate recommendation error: {e}")
            recommended_candidates = []

    return render(request, 'employer_dashboard.html', {
        'jobs': Job.objects.filter(employer=request.user),
        'total_applications': Application.objects.filter(job__employer=request.user).count(),
        'recommended_candidates': recommended_candidates,  # ✅ ADDED
    })


@login_required
def employer_profile(request):
    if request.user.profile.user_type != 'employer':
        return HttpResponseForbidden("Access denied")

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('jobs:employer_dashboard')
    else:
        form = EmployerProfileForm(instance=request.user.profile)

    return render(request, 'employer_profile.html', {'form': form})


@login_required
def post_job(request):
    if request.user.profile.user_type != 'employer':
        return HttpResponseForbidden("Access denied")

    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully')
            return redirect('jobs:employer_dashboard')
    else:
        form = JobPostForm()

    return render(request, 'post_job.html', {'form': form})


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated')
            return redirect('jobs:employer_dashboard')
    else:
        form = JobPostForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted')
        return redirect('jobs:employer_dashboard')

    return render(request, 'delete_job_confirm.html', {'job': job})


@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = Application.objects.filter(job=job)
    
    # ✅ ADDED: Get recommended candidates for this specific job
    recommended_candidates = []
    try:
        recommended_candidates = get_candidate_recommendations(job, count=8)
    except Exception as e:
        print(f"Candidate recommendation error: {e}")
        recommended_candidates = []
    
    return render(request, 'view_applications.html', {
        'job': job,
        'applications': applications,
        'recommended_candidates': recommended_candidates,  # ✅ ADDED
    })


@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Application.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(
                request,
                f'Status updated to {application.get_status_display()}'
            )

    return redirect('jobs:view_applications', job_id=application.job.id)