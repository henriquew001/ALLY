# /home/heinrich/projects/ConsciousFit/frontend/cofi/accounts/admin.py

from django.contrib import admin
from .models import UserPackage, CustomUser

class UserPackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'start_date', 'end_date', 'is_active', 'canceled_at', 'next_payment_at')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'package__name')
    readonly_fields = ('start_date',)

admin.site.register(UserPackage, UserPackageAdmin)
admin.site.register(CustomUser)
