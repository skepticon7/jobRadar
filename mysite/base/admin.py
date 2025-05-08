from django.contrib import admin
from .models import Job, Application, User
from django.contrib.auth.admin import UserAdmin


# Personnalisation du modèle User si nécessaire
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_recruiter', 'is_staff']
    list_filter = ['is_recruiter', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_recruiter', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_recruiter'),
        }),
    )


# Enregistrer les modèles
admin.site.register(User, CustomUserAdmin)
admin.site.register(Job)
admin.site.register(Application)


