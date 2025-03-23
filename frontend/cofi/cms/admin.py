# /home/heinrich/projects/ConsciousFit/frontend/cofi/cms/admin.py

from django.contrib import admin
from .models import Lesson, AdditionalMaterial, Package

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'active', 'is_popular', 'order', 'is_lifetime', 'duration', 'duration_unit', 'is_recurring', 'discount', 'discount_start_date', 'discount_end_date')
    list_filter = ('active', 'is_popular', 'is_lifetime', 'duration_unit', 'is_recurring')
    search_fields = ('name', 'short_description', 'description')
    exclude = ('slug',)
    filter_horizontal = ('additional_materials', 'lessons')

admin.site.register(Lesson)
admin.site.register(AdditionalMaterial)
admin.site.register(Package, PackageAdmin)
