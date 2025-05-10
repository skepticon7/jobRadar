from email.policy import default

from django import forms
from django.core.exceptions import ValidationError
from . import models
from django import forms

from django import forms
from django import forms
from .models import Resume



def validate_cv_file(file):
    import os
    ALLOWED_CV_EXTENSIONS = ['.docx', '.doc', '.pdf', '.txt', '.odt', '.rtf']

    ext = os.path.splitext(file.name)[1].lower()       
    if ext not in ALLOWED_CV_EXTENSIONS:
        raise ValidationError(f"Unsupported file extension: {ext}.")



class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['filePath']

    def clean_filePath(self):
        file = self.cleaned_data.get('filePath')
        if file:
            try:
                validate_cv_file(file)
            except ValidationError as e:
                raise forms.ValidationError(str(e)) 
        return file
    


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe'
        })
    )



class CreateUser(forms.ModelForm):
    USER_TYPES = [
        ('jobSeeker', 'Job Seeker'),
        ('recruiter', 'Recruiter')
    ]

    confirmed_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        initial='jobSeeker',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'userType'
        })
    )
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control recruiter-field',
            'placeholder': 'Enter company name'
        })
    )

    position_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control recruiter-field',
            'placeholder': 'Enter position title '
        })
    )

    department = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control recruiter-field',
            'placeholder': 'Enter department name'
        })
    )


    class Meta:
        model = models.JobSeeker
        fields = ['name', 'email' , 'phone_number','profession' ,'password','confirmed_password' ,  'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),

            'profession': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your profession'
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirmed_password')

        if password and confirmed_password:
            if password != confirmed_password:
                raise ValidationError("Passwords do not match")

        return cleaned_data

class CreateJobPost(forms.ModelForm):
    class Meta:
        model = models.JobPost
        fields = ['title' , 'location' , 'status' , 'show_salary' , 'min_education' , 'experience_level' , 'salary_min' , 'salary_max']


# class CreateUserSettings(forms.ModelForm):
#     class Meta:
#         model = models.JobSeeker
#         fields = '__all__'

class CreateRecruiterSettings(forms.ModelForm):
    class Meta:
        model = models.Recruiter
        fields = ['name' , 'email' , 'phone_number' , 'profession' , 'position_title' , 'department' , 'company_name' , 'profile_picture' ]



