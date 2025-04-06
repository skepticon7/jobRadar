from django.contrib.auth.models import AbstractUser
from django.db import models

# ----------------------------
# COMPANY MODEL
# ----------------------------
class Company(models.Model):
    name = models.CharField(max_length=75, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=False, max_length=191)
    industry = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'address')

# ----------------------------
# BASE USER MODEL
# ----------------------------
class BaseUser(AbstractUser):
    username = None  # Remove default username
    name = models.CharField(max_length=75, null=False)
    email = models.EmailField(max_length=191, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Remove default group/permission fields unless you're using them
    groups = None
    user_permissions = None

    class Meta:
        abstract = True

# ----------------------------
# JOB SEEKER MODEL
# ----------------------------
class JobSeeker(BaseUser):
    phone_number = models.CharField(max_length=15, unique=True, null=False)

# ----------------------------
# COMPANY USER (For Authentication)
# ----------------------------
class CompanyUser(BaseUser):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='admin_user', null=False, blank=False)
    # This is the person who registered the company and manages it

# ----------------------------
# DEPARTMENT MODEL
# ----------------------------
class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=75, null=False, blank=False)

    class Meta:
        unique_together = ('company', 'name')

# ----------------------------
# RECRUITER MODEL (Created by Company)
# ----------------------------
class Recruiter(BaseUser):
    position_title = models.CharField(max_length=191, null=False)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='recruiters', null=False)

# ----------------------------
# JOB POST MODEL
# ----------------------------
class JobPost(models.Model):
    ONGOING = 'ongoing'
    TERMINATED = 'terminated'

    STATUS_CHOICES = [
        (ONGOING, 'Ongoing'),
        (TERMINATED, 'Terminated')
    ]

    title = models.CharField(max_length=75, null=False)
    description = models.TextField(max_length=191, null=False)
    location = models.CharField(max_length=75, null=False)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='job_posts')
    status = models.CharField(default=ONGOING, max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title', 'recruiter', 'status')

# ----------------------------
# RESUME MODEL
# ----------------------------
class Resume(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='resumes')
    filePath = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ----------------------------
# APPLICATION MODEL
# ----------------------------
class Application(models.Model):
    PENDING = 'pending'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
    ]

    jobPost = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='my_applications')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('jobPost', 'jobSeeker')
