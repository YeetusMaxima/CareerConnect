import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from django.db.models import Count, Q
from .models import Job, Application, SavedJob, UserProfile


class JobRecommender:
    """KNN-based job recommendation system for job seekers"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.job_features = None
        self.job_ids = None
        
    def prepare_job_features(self, jobs):
        """Convert jobs into numerical features for KNN"""
        features = []
        job_ids = []
        
        categories = list(set([job.category for job in jobs]))
        job_types = list(set([job.job_type for job in jobs]))
        locations = list(set([job.location for job in jobs]))
        
        for job in jobs:
            category_encoded = categories.index(job.category)
            job_type_encoded = job_types.index(job.job_type)
            location_encoded = locations.index(job.location) if job.location in locations else 0
            
            experience = job.experience_required
            salary = (job.salary_min + job.salary_max) / 2 if job.salary_min and job.salary_max else 0
            
            feature_vector = [
                category_encoded,
                job_type_encoded,
                experience,
                salary,
                location_encoded
            ]
            
            features.append(feature_vector)
            job_ids.append(job.id)
        
        return np.array(features), job_ids
    
    def prepare_user_preferences(self, user):
        """Extract user preferences based on their profile and activity"""
        profile = user.profile
        applications = Application.objects.filter(applicant=user)
        
        if applications.exists():
            applied_jobs = [app.job for app in applications]
            categories = [job.category for job in applied_jobs]
            most_common_category = max(set(categories), key=categories.count) if categories else 'it'
            avg_experience = sum([job.experience_required for job in applied_jobs]) / len(applied_jobs)
            job_types = [job.job_type for job in applied_jobs]
            most_common_type = max(set(job_types), key=job_types.count) if job_types else 'full-time'
            preferred_location = profile.location if profile.location else applied_jobs[0].location
        else:
            most_common_category = 'it'
            avg_experience = profile.experience_years
            most_common_type = 'full-time'
            preferred_location = profile.location if profile.location else ''
        
        return {
            'category': most_common_category,
            'job_type': most_common_type,
            'experience': avg_experience,
            'location': preferred_location
        }
    
    def get_recommendations(self, user, n_recommendations=6):
        """Get job recommendations for a user using KNN algorithm"""
        applied_job_ids = Application.objects.filter(applicant=user).values_list('job_id', flat=True)
        saved_job_ids = SavedJob.objects.filter(user=user).values_list('job_id', flat=True)
        excluded_ids = list(applied_job_ids) + list(saved_job_ids)
        
        available_jobs = Job.objects.filter(is_active=True).exclude(id__in=excluded_ids)
        
        if not available_jobs.exists():
            return []
        
        job_features, job_ids = self.prepare_job_features(available_jobs)
        
        if len(job_features) == 0:
            return []
        
        job_features_scaled = self.scaler.fit_transform(job_features)
        user_prefs = self.prepare_user_preferences(user)
        
        jobs_list = list(available_jobs)
        categories = list(set([job.category for job in jobs_list]))
        job_types = list(set([job.job_type for job in jobs_list]))
        locations = list(set([job.location for job in jobs_list]))
        
        category_encoded = categories.index(user_prefs['category']) if user_prefs['category'] in categories else 0
        job_type_encoded = job_types.index(user_prefs['job_type']) if user_prefs['job_type'] in job_types else 0
        location_encoded = locations.index(user_prefs['location']) if user_prefs['location'] in locations else 0
        
        user_vector = np.array([[
            category_encoded,
            job_type_encoded,
            user_prefs['experience'],
            0,
            location_encoded
        ]])
        
        user_vector_scaled = self.scaler.transform(user_vector)
        
        n_neighbors = min(n_recommendations, len(job_features))
        knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
        knn.fit(job_features_scaled)
        
        distances, indices = knn.kneighbors(user_vector_scaled)
        recommended_job_ids = [job_ids[i] for i in indices[0]]
        recommended_jobs = Job.objects.filter(id__in=recommended_job_ids)
        
        recommended_jobs_sorted = sorted(
            recommended_jobs,
            key=lambda job: recommended_job_ids.index(job.id)
        )
        
        return recommended_jobs_sorted


# ✅ NEW: Candidate Recommender for Employers
class CandidateRecommender:
    """KNN-based candidate recommendation system for employers"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def prepare_candidate_features(self, candidates):
        """Convert candidate profiles into numerical features"""
        features = []
        candidate_ids = []
        
        # Get all unique values for encoding
        all_locations = list(set([c.location if c.location else '' for c in candidates]))
        
        for candidate in candidates:
            # Experience years
            experience = candidate.experience_years
            
            # Location encoding
            location_encoded = all_locations.index(candidate.location) if candidate.location in all_locations else 0
            
            # Skills count (rough measure of qualification)
            skills_count = len(candidate.skills.split(',')) if candidate.skills else 0
            
            # Has resume
            has_resume = 1 if candidate.resume else 0
            
            # Education length (rough measure)
            education_length = len(candidate.education) if candidate.education else 0
            
            feature_vector = [
                experience,
                location_encoded,
                skills_count,
                has_resume,
                min(education_length / 100, 10)  # Normalize
            ]
            
            features.append(feature_vector)
            candidate_ids.append(candidate.user.id)
        
        return np.array(features), candidate_ids
    
    def prepare_job_requirements(self, job):
        """Extract job requirements as a feature vector"""
        # Get all candidates to get location list
        all_profiles = UserProfile.objects.filter(user_type='seeker')
        all_locations = list(set([p.location if p.location else '' for p in all_profiles]))
        
        location_encoded = all_locations.index(job.location) if job.location in all_locations else 0
        
        # Required skills count
        required_skills = len(job.skills_required.split(',')) if job.skills_required else 0
        
        return {
            'experience': job.experience_required,
            'location': location_encoded,
            'skills_count': required_skills,
            'has_resume': 1,  # Prefer candidates with resumes
            'education': 5  # Mid-range preference
        }
    
    def get_recommendations(self, job, n_recommendations=10):
        """Get candidate recommendations for a job using KNN"""
        # Get all job seekers who haven't applied to this job
        applied_user_ids = Application.objects.filter(job=job).values_list('applicant_id', flat=True)
        
        available_candidates = UserProfile.objects.filter(
            user_type='seeker'
        ).exclude(user_id__in=applied_user_ids).select_related('user')
        
        if not available_candidates.exists():
            return []
        
        candidate_features, candidate_ids = self.prepare_candidate_features(available_candidates)
        
        if len(candidate_features) == 0:
            return []
        
        candidate_features_scaled = self.scaler.fit_transform(candidate_features)
        job_reqs = self.prepare_job_requirements(job)
        
        # Get location list again for encoding
        all_locations = list(set([c.location if c.location else '' for c in available_candidates]))
        
        job_vector = np.array([[
            job_reqs['experience'],
            job_reqs['location'],
            job_reqs['skills_count'],
            job_reqs['has_resume'],
            job_reqs['education']
        ]])
        
        job_vector_scaled = self.scaler.transform(job_vector)
        
        n_neighbors = min(n_recommendations, len(candidate_features))
        knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
        knn.fit(candidate_features_scaled)
        
        distances, indices = knn.kneighbors(job_vector_scaled)
        recommended_candidate_ids = [candidate_ids[i] for i in indices[0]]
        
        # Get User objects
        from django.contrib.auth.models import User
        recommended_candidates = User.objects.filter(
            id__in=recommended_candidate_ids
        ).select_related('profile')
        
        # Sort by match quality (distance)
        recommended_candidates_sorted = sorted(
            recommended_candidates,
            key=lambda c: recommended_candidate_ids.index(c.id)
        )
        
        return recommended_candidates_sorted


# Convenience functions
def get_job_recommendations(user, count=6):
    """Get job recommendations for a job seeker"""
    recommender = JobRecommender()
    return recommender.get_recommendations(user, n_recommendations=count)


def get_candidate_recommendations(job, count=10):
    """Get candidate recommendations for a job posting"""
    recommender = CandidateRecommender()
    return recommender.get_recommendations(job, n_recommendations=count)