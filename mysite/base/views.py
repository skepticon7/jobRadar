
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import ApplicationForm  # Assure-toi que l'import est correct
from .forms import CustomUserCreationForm  # Import du formulaire personnalisé
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('job_list')  # Redirige vers la liste des emplois après connexion
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('job_list')  # Redirige vers la liste des emplois après la déconnexion

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})



@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    User = get_user_model()  # Récupère le modèle User

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, request.POST)

        if form.is_valid():
            application = form.save(commit=False)

            # Vérifie si request.user est une instance correcte
            if isinstance(request.user, User):
                application.user = request.user  # Assignation correcte de l'utilisateur
                application.job = job
                application.save()

                return redirect('job_list')
            else:
                return render(request, 'apply_job.html', {'job': job, 'form': form, 'error': 'Utilisateur invalide'})

    else:
        form = ApplicationForm()

    return render(request, 'apply_job.html', {'job': job, 'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('job_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_job.html', {'form': form})  # Assure-toi que le template est correct
