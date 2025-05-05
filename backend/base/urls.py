from django.urls import path
from . import views
from .views import LoginView, LogoutView
app_name = 'jobradar'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('jobPosts/' , views.JobPosts.as_view(), name='jobPosts'),
    path('jobPost/<int:id>' , views.JobPostDetail.as_view(), name='jobPost'),
    path('/posts' , views.Posts.as_view() , name='posts'),
    path('signup/' , views.Signup.as_view() , name='user-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/success/', views.RegisterSuccess.as_view(), name='register-success'),
    path('deleteJobPost/<int:id>' , views.JobPostDelete.as_view() , name='delete-jobpost'),
    path('updateJobPost/<int:id>' , views.JobPostUpdate.as_view() , name='update-jobpost'),
    path('settings' , views.Settings.as_view() , name='settings')
]