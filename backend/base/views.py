from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateUser
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout

from .models import Recruiter, JobSeeker

logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.views import View
from django.contrib import messages

from django.views import View
from django.shortcuts import render, redirect
from .models import JobSeeker, Recruiter
from .forms import LoginForm
from django.contrib import messages

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Vérifier dans JobSeeker
            try:
                user = JobSeeker.objects.get(email=email)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['user_type'] = 'jobseeker'
                    request.session['user_name'] = user.name
                    request.session['profile_picture'] = user.profile_picture.url
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('jobradar:home')
            except JobSeeker.DoesNotExist:
                pass

            # Vérifier dans Recruiter
            try:
                user = Recruiter.objects.get(email=email)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['user_type'] = 'recruiter'
                    request.session['user_name'] = user.name
                    request.session['profile_picture'] = user.profile_picture.url
                    return redirect('jobradar:home')
            except Recruiter.DoesNotExist:
                pass

            form.add_error(None, 'Email ou mot de passe invalide.')

        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        request.session.flush()  # Supprimer toutes les données de session
        return redirect('jobradar:login')

# class listjob(View):
#     def get(self, request):
#         job_posts = JobPost.objects.all()
#         return render(request, 'listjob.html', {'job_posts': job_posts})





# Create your views here.
class Home(View):
    def get(self, request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture':profilePicture
        }
        return render(request, 'home.html' , context)

class RegisterSuccess(View):
    def get(self , request):
        return render(request , 'register_success.html')

class Signup(View):
    signup_template = 'signup.html'
    def get(self , request):
        form = CreateUser()
        return render(request, self.signup_template , {'form' : form})

    def post(self, request):
        form = CreateUser(request.POST, request.FILES)
        if form.is_valid():
            user_data = form.cleaned_data
            user_type = user_data.pop('user_type')
            user_data['password'] = make_password(user_data['password'])
            user_data.pop('confirmed_password')
            try:
                if user_type == 'jobSeeker':
                    user_data.pop('company_name')
                    user_data.pop('position_title')
                    user_data.pop('department')
                    jobSeeker = JobSeeker.objects.create(**user_data)
                    jobSeeker.save()
                    return redirect('jobradar:register-success')
                elif user_type == 'recruiter':
                    companyMan = Recruiter.objects.create(**user_data)
                    companyMan.save()
                    return redirect('jobradar:register-success')
            except Exception as e:
                print(f'Error creating user: {str(e)}')
                form.add_error(None, "error saving user to database")
        return render(request, self.signup_template, {'form': form})

class Posts(View):
    def get(self , request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture': profilePicture
        }
        return render(request , 'posts.html' , context)