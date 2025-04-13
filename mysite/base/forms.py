from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Job, Application
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Utilise ton modèle personnalisé
        fields = ['username', 'email', 'password1', 'password2']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter','Email']


