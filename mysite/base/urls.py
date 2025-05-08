from django.urls import path
from .views import job_list, job_detail, apply_for_job, register
from .views import custom_login,custom_logout

urlpatterns = [
    path('', job_list, name='job_list'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', apply_for_job, name='apply_for_job'),
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
]
