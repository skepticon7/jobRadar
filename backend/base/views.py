from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateUser
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
import logging

from .models import Recruiter, JobSeeker

logger = logging.getLogger(__name__)


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'hello.html')

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