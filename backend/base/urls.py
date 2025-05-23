from django.urls import path
from . import views
from .views import LoginView, LogoutView
app_name = 'jobradar'
urlpatterns = [
    path('' , views.JobPosts.as_view(), name='jobPosts'),
    path('jobPost/<int:id>' , views.JobPostDetail.as_view(), name='jobPost'),
    path('posts' , views.Posts.as_view() , name='posts'),
    path('signup/' , views.Signup.as_view() , name='user-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/success/', views.RegisterSuccess.as_view(), name='register-success'),
    path('deleteJobPost/<int:id>' , views.JobPostDelete.as_view() , name='delete-jobpost'),
    path('updateJobPost/<int:id>' , views.JobPostUpdate.as_view() , name='update-jobpost'),
    # path('apply-job/<int:id>',views.apply_job.as_view(), name='apply-job'),
    path('jobpost/<int:post_id>/applications/', views.ViewApplications.as_view(), name='view-applications'),
    path('applications/' , views.Applications.as_view() , name='applications'),
    path('deleteApplication/<int:id>' , views.deleteApplication.as_view() , name='delete-application'),
    path('application/<int:app_id>/update-status/', views.UpdateApplicationStatus.as_view(), name='update-application-status'),
    path('settings' , views.Settings.as_view() , name='settings'),
    path('deleteResume/<int:id>/', views.ResumeDelete.as_view(), name='deleteresume'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('settings' , views.Settings.as_view() , name='settings')
]