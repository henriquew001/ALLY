# /home/heinrich/projects/ConsciousFit/frontend/cofi/cms/models.py

from django.db import models
from django.utils.text import slugify

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_example = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class AdditionalMaterial(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_example = models.BooleanField(default=False)
    packages = models.ManyToManyField('Package', blank=True)

    def __str__(self):
        return self.title

class Package(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    active = models.BooleanField(default=True)
    is_recurring = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    duration = models.IntegerField(blank=True, null=True)
    duration_unit = models.CharField(max_length=50, choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], default='days')
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    discount_start_date = models.DateField(blank=True, null=True)
    discount_end_date = models.DateField(blank=True, null=True)
    additional_materials = models.ManyToManyField(AdditionalMaterial, related_name='included_in_packages', blank=True)
    lessons = models.ManyToManyField('Lesson', related_name='included_in_packages', blank=True)
    is_lifetime = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
