# cms/admin.py

from django.contrib import admin
from .models import Recipe, Lesson, AdditionalMaterial, Package, UserPackage

admin.site.register(Recipe)
admin.site.register(Lesson)
admin.site.register(AdditionalMaterial)
admin.site.register(Package)
admin.site.register(UserPackage)
