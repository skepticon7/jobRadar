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

    EDUCATION_CHOICES = [
        ('high_school', 'High School'),
        ('diploma', 'Diploma'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', 'PhD'),
    ]

    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (2-5 years)'),
        ('senior', 'Senior Level (5+ years)'),
        ('executive', 'Executive Level'),
    ]

    SALARY_STATUS_CHOICE = [
        ('SHOW' , 'Show salary'),
        ('HIDE' , 'Hide salary')
    ]

    title = models.CharField(max_length=75, null=False)
    location = models.CharField(max_length=75, null=False)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='job_posts')
    status = models.CharField(default=ONGOING, max_length=20, choices=STATUS_CHOICES)

    min_education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
        default='bachelor',
        verbose_name="Minimum Education Required"
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='mid',
        verbose_name="Experience Level Required"
    )

    # Salary Information
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Minimum Salary"
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Maximum Salary"
    )

    show_salary = models.CharField(max_length=20, choices=SALARY_STATUS_CHOICE)


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
