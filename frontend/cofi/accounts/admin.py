from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    # Customize the admin interface for CustomUser here
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active')}),  # Modified: Added email, removed username, added is_active
        (_('Personal Info'), {'fields': ('username', 'first_name', 'last_name')}), # Modified: Added username
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'), # Modified: Removed is_active
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')}
         ),
    )
    search_fields = ['email']
    ordering = ['email']
