from django.urls import path
from . import views
from .views import LoginView, LogoutView
app_name = 'jobradar'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('signup/' , views.Signup.as_view() , name='user-signup'),
      path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/success/', views.RegisterSuccess.as_view(), name='register-success'),
]