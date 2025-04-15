from django.contrib.auth.models import AbstractUser
from django.db import models


# ----------------------------
# BASE USER MODEL
# ----------------------------
class BaseUser(AbstractUser):
    username = None  # Remove default username
    name = models.CharField(max_length=75, null=False)
    email = models.EmailField(max_length=191, unique=True, null=False)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/' , default = 'profile_picture/default.jpg' , null=False, blank=False)
    profession = models.CharField(max_length=100, null=False , blank=False)
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
    pass
# ----------------------------
# RECRUITER MODEL (Created by Company)
# ----------------------------
class Recruiter(BaseUser):
    position_title = models.CharField(max_length=191, null=False)
    department = models.CharField(max_length=191, null=False)
    company_name = models.CharField(max_length=191, null=False)
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
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    motivation_letter = models.TextField(null=False)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('jobPost', 'jobSeeker')
