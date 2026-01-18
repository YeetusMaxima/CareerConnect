from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Job, Application, Contact


class UserRegistrationForm(UserCreationForm):
    """User registration form with user type selection"""
    
    # ✅ ADDED: Full Name Fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email'
        })
    )
    
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your phone number',
            'type': 'tel'
        })
    )
    
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPES,
        widget=forms.RadioSelect,
        required=True
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']  # ✅ Added names
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm password'
        })


class JobSeekerProfileForm(forms.ModelForm):
    """Job seeker profile update form"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'location', 'bio', 'profile_picture', 'resume', 
                  'skills', 'experience_years', 'education']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Python, Django, JavaScript'}),
            'education': forms.Textarea(attrs={'rows': 4}),
        }


class EmployerProfileForm(forms.ModelForm):
    """Employer profile update form"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'location', 'company_name', 'company_website', 
                  'company_logo', 'company_description']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }


class JobPostForm(forms.ModelForm):
    """Job posting form for employers"""
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'company_logo', 'description', 
                  'responsibilities', 'requirements', 'category', 'job_type', 
                  'location', 'salary_min', 'salary_max', 'experience_required', 
                  'skills_required', 'deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'skills_required': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Python, Django, React'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class JobApplicationForm(forms.ModelForm):
    """Job application form"""
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter', 'contact_email', 'contact_phone']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your cover letter here...'}),
        }


class JobSearchForm(forms.Form):
    """Job search and filter form"""
    keyword = forms.CharField(max_length=100, required=False, 
                              widget=forms.TextInput(attrs={'placeholder': 'Job title, keywords...'}))
    location = forms.CharField(max_length=100, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Location...'}))
    category = forms.ChoiceField(choices=[('', 'All Categories')] + list(Job.CATEGORIES), 
                                 required=False)
    job_type = forms.ChoiceField(choices=[('', 'All Types')] + list(Job.JOB_TYPES), 
                                 required=False)
    min_salary = forms.DecimalField(required=False, min_value=0,
                                    widget=forms.NumberInput(attrs={'placeholder': 'Min salary'}))


class ContactForm(forms.ModelForm):
    """Contact form"""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
        }