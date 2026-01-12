from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """Extended user profile for job seekers and employers"""
    USER_TYPES = (
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Job Seeker specific fields
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, help_text="Comma separated skills")
    experience_years = models.IntegerField(default=0)
    education = models.TextField(blank=True)
    
    # Employer specific fields
    company_name = models.CharField(max_length=200, blank=True)
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class Job(models.Model):
    """Job posting model"""
    JOB_TYPES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    
    CATEGORIES = (
        ('it', 'IT & Software'),
        ('business', 'Business'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('engineering', 'Engineering'),
        ('other', 'Other'),
    )
    
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_posted')
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='job_logos/', blank=True, null=True)
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    location = models.CharField(max_length=100)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    experience_required = models.IntegerField(default=0, help_text="Years of experience")
    skills_required = models.TextField(help_text="Comma separated skills")
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-posted_date']
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"
    
    def salary_range(self):
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,.0f} - ${self.salary_max:,.0f}"
        elif self.salary_min:
            return f"${self.salary_min:,.0f}+"
        return "Negotiable"


class Application(models.Model):
    """Job application model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='application_resumes/')
    cover_letter = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ['job', 'applicant']
    
    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"


class SavedJob(models.Model):
    """Saved jobs by job seekers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'job']
    
    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


class Contact(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"