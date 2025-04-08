from django.urls import path
from . import views

app_name = 'jobradar'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('signup/' , views.Signup.as_view() , name='user-signup'),
    path('signup/success/', views.RegisterSuccess.as_view(), name='register-success'),
]