from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Customize the admin interface for CustomUser here
    list_display = ('email', 'username', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_active',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
