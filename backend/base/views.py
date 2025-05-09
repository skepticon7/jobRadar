from django.db.utils import IntegrityError
from django.db.models import Count
from .forms import CreateUser , CreateJobPost
from django.contrib.auth.hashers import make_password
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth import login
from .models import JobSeeker, Recruiter
from .forms import LoginForm
from .forms import ResumeForm
from .models import Resume
from django.views import View
import os
from django.contrib.auth.models import User
from django.contrib import messages
from .models import JobPost, JobSeeker, Resume, Application
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPost, JobSeeker, Resume, Application
from django.views.decorators.csrf import csrf_exempt
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, Application
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import JobPost, Application

class ViewApplications(View):
    def get(self, request, post_id):
        # Vérifie si l'utilisateur est connecté
        if not request.session.get('user_id'):
            return redirect('jobradar:login')

        # Données de session
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        user_fullname = request.session.get('user_name')
        profile_picture = request.session.get('profile_picture')

        # Vérifie que l'utilisateur est un recruteur
        if user_type != 'recruiter':
            return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")

        # Récupère le poste du recruteur
        job_post = get_object_or_404(JobPost, id=post_id, recruiter_id=user_id)

        # Récupère toutes les candidatures liées à ce poste
        applications = job_post.applications.select_related('jobSeeker', 'resume')

        # Contexte transmis au template
        context = {
            'job_post': job_post,
            'applications': applications,
            'context': {
                'user_fullname': user_fullname,
                'user_type': user_type,
                'profile_picture': profile_picture,
                'user_id': user_id,
            }
        }

        return render(request, 'view_applications.html', context)



class UpdateApplicationStatus(View):
    def post(self, request, app_id):
        # Vérification de session : utilisateur connecté ?
        if not request.session.get('user_id'):
            return redirect('jobradar:login')

        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')

        # Autorisation : uniquement les recruteurs
        if user_type != 'recruiter':
            return HttpResponseForbidden("Vous n'avez pas la permission de modifier cette candidature.")

        # Récupération de la candidature et de l'offre associée
        application = get_object_or_404(Application, id=app_id)
        job_post = application.jobPost

        # Vérification que le recruteur est le propriétaire de l'offre
        if job_post.recruiter.id != user_id:
            return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette candidature.")

        # Mise à jour du statut de la candidature
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()

        # Redirection vers la page des candidatures
        return redirect('jobradar:view-applications', post_id=job_post.id)



# @csrf_exempt
# def apply_job(request, id):
#     if request.method == 'POST':
#         if not request.session.get('user_id'):
#             return redirect('jobradar:login')
#
#         user_id = request.session.get('user_id')
#         resume_id = request.POST.get('resume_id')
#         motivation_letter = request.POST.get('motivation')
#
#         try:
#             job = get_object_or_404(JobPost, id=id)
#             job_seeker = get_object_or_404(JobSeeker, id=user_id)
#             resume = get_object_or_404(Resume, id=resume_id, jobSeeker=job_seeker)
#
#             existing_application = Application.objects.filter(jobPost=job, jobSeeker=job_seeker).first()
#             if existing_application:
#                 return redirect(f'/jobPost/{id}?success=already')
#
#             Application.objects.create(
#                 jobPost=job,
#                 jobSeeker=job_seeker,
#                 resume=resume,
#                 motivation_letter=motivation_letter
#             )
#             return redirect(f'/jobPost/{id}?success=1')
#
#         except Exception as e:
#             print("Erreur :", e)
#             return redirect(f'/jobPost/{id}?success=0')
#
#     return redirect(f'/jobPost/{id}')


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
                    return redirect('jobradar:jobPosts')
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





class Home(View):
    def get(self, request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        print("here in home")
        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture':profilePicture
        }
        return render(request, 'home.html' , {'context' : context})


class JobPosts(View):
    def get(self , request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        print("here in jobposts")
        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture': profilePicture
        }
        job_posts = JobPost.objects.all().select_related('recruiter')
        return render(request , 'jobOffers.html' , {'job_posts' : job_posts , 'context' : context})

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


from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPost, Resume, JobSeeker

class JobPostDetail(View):
    def get(self, request, id):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')

        user_id = request.session.get('user_id')
        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')

        jobPost = get_object_or_404(JobPost, id=id)

        resumes = []
        hasApplied = True if Application.objects.filter(jobSeeker_id = user_id , jobPost_id = id).exists() else False
        if user_type == 'jobseeker':
            try:
                jobseeker = JobSeeker.objects.get(id=user_id)
                resumes = Resume.objects.filter(jobSeeker=jobseeker)
            except JobSeeker.DoesNotExist:
                resumes = []

        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture': profilePicture,
            'resumes': resumes
        }

        return render(request, 'job_detail.html', {'job': jobPost, 'context': context , 'hasApplied': hasApplied})

    def post(self , request , id):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        user_id = request.session.get('user_id')
        jobPost = get_object_or_404(JobPost, id=id)
        resume_id = request.POST.get('resume_id')
        motivation_letter = request.POST.get('motivation')

        if resume_id:
            try:
                resume = Resume.objects.get(id=resume_id, jobSeeker_id=user_id)
                Application.objects.create(
                    jobPost=jobPost,
                    jobSeeker_id=user_id,
                    resume=resume,
                    motivation_letter=motivation_letter
                )
                messages.success(request, "Application submitted successfully.")
            except Resume.DoesNotExist:
                messages.error(request, "CV Doesnt exist")
        else:
            messages.error(request, "You have to select a CV")

        return redirect(f"/jobPost/{id}")


class Posts(View):
    def get(self , request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        user_id = request.session.get('user_id')
        posts = JobPost.objects.filter(recruiter_id = user_id).annotate(total_posts=Count('applications'))
        form = CreateJobPost()
        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture': profilePicture,
            'user_id':user_id
        }
        return render(request , 'posts.html' , {'posts' : posts , 'context' : context , 'form' : form})

    def post(self, request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        form = CreateJobPost(request.POST)
        print("here in post before")
        print(form.is_valid())
        if form.is_valid():
            print("here in post")
            try:
                jobPostData = form.cleaned_data
                jobPostData['recruiter_id'] = request.session.get('user_id')
                jobPost = JobPost.objects.create(**jobPostData)
                jobPost.save()
                return redirect('jobradar:posts')
            except IntegrityError as e:
                print(f"error saving new job : {str(e)}")
                messages.error(request, "A job with the same title already exists. Please choose a different title.")
                return redirect('jobradar:posts')
        else:
            form.add_error(None, 'Invalid form submission. Please check your inputs.')
            return render(request, 'posts.html', {'form': form})

class JobPostDelete(View):
    def get(self , request , id):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        jobPost = JobPost.objects.get(id = id)
        jobPost.delete()
        return redirect('jobradar:posts')

class JobPostUpdate(View):
    def post(self , request , id):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        jobPost = JobPost.objects.get(id = id)
        form = CreateJobPost(request.POST , instance=jobPost)
        if form.is_valid():
            form.save()
            return redirect('jobradar:posts')
        form.add_error(None, 'Invalid form submission.')
        return render(request, 'posts.html', {'form': form})


class Applications(View):
    def get(self , request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        user_id = request.session.get('user_id')

        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture': profilePicture,
            'user_id': user_id
        }

        applications = Application.objects.filter(jobSeeker_id=user_id)

        return render(request, 'applications.html', {'context': context , 'applications':applications})


class deleteApplication(View):
    def get(self , request , id):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')
        application = Application.objects.get(id = id)
        application.delete()
        return redirect('jobradar:applications')


"""
    Add : CV extensions to only :  (.docx, .doc, .pdf, .txt, .odt, .rtf)
    Function get call in : form.is_valid()
"""

class Settings(View):

    def get(self, request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')

        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        user_id = request.session.get('user_id')

        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture': profilePicture,
            'user_id': user_id
        }

        if user_type == 'jobseeker':
            user = JobSeeker.objects.get(id=user_id)
            resumes = Resume.objects.filter(jobSeeker=user)
            resume_form = ResumeForm()
            context.update({'user': user, 'resumes': resumes, 'resume_form': resume_form})
        else:
            user = Recruiter.objects.get(id=user_id)
            context.update({'user': user})

        return render(request, 'settings.html', {'context': context})

    def post(self, request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')

        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')

        if user_type == 'jobseeker':
            jobseeker = JobSeeker.objects.get(id=user_id)
            form = ResumeForm(request.POST, request.FILES)
            
            if form.is_valid():
                resume = form.save(commit=False)
                resume.jobSeeker = jobseeker
                resume.save()
                messages.success(request, "CV ajouté avec succès.")
            else:
                messages.error(request, "Erreur lors de l'ajout du CV. Vérifiez le format du fichier.")
        
        return redirect('jobradar:settings')
    



"""
    Profile :
"""

# @login_required(login_url='jobradar:login')

class Profile(View):

    def get(self, request):
        if not request.session.get('user_id'):
            return redirect('jobradar:login')

        user_fullname = request.session.get('user_name')
        user_type = request.session.get('user_type')
        profilePicture = request.session.get('profile_picture')
        user_id = request.session.get('user_id')

        context = {
            'user_fullname': user_fullname,
            'user_type': user_type,
            'profile_picture': profilePicture,
            'user_id': user_id
        }

        if user_type == 'jobseeker':
            user = JobSeeker.objects.get(id=user_id)
            resumes = Resume.objects.filter(jobSeeker=user)

            recent_applications = Application.objects.filter(jobSeeker=user).order_by('-created_at')[:5]
            applications_count = Application.objects.filter(jobSeeker=user).count()
            
            context.update({
                'user': user, 
                'resumes': resumes,
                'recent_applications': recent_applications,
                'applications_count': applications_count,
                'profile_views': 0  
            })
        else:
            user = Recruiter.objects.get(id=user_id)

            recent_job_posts = JobPost.objects.filter(recruiter=user).order_by('-created_at')[:5]
            job_posts_count = JobPost.objects.filter(recruiter=user).count()
            active_jobs = JobPost.objects.filter(recruiter=user, status='ongoing').count()
 
            applications_received = Application.objects.filter(jobPost__recruiter=user).count()
            
            context.update({
                'user': user,
                'recent_job_posts': recent_job_posts,
                'job_posts_count': job_posts_count,
                'applications_received': applications_received,
                'active_jobs': active_jobs
            })

        return render(request, 'profile.html', {'context': context}) 

    








    