# /home/heinrich/projects/ConsciousFit/frontend/cofi/cms/models.py

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    is_example = models.BooleanField(default=False, verbose_name=_("Is Example"))

    def __str__(self):
        return self.title

class AdditionalMaterial(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    is_example = models.BooleanField(default=False, verbose_name=_("Is Example"))
    packages = models.ManyToManyField('Package', blank=True, verbose_name=_("Packages"))

    def __str__(self):
        return self.title

class Package(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name=_("Slug"))
    short_description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Short Description"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    image = models.ImageField(upload_to='packages/', blank=True, null=True, verbose_name=_("Image"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    is_recurring = models.BooleanField(default=False, verbose_name=_("Is Recurring"))
    is_popular = models.BooleanField(default=False, verbose_name=_("Is Popular"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    duration = models.IntegerField(blank=True, null=True, verbose_name=_("Duration"))
    duration_unit = models.CharField(max_length=50, choices=[('days', _('Days')), ('weeks', _('Weeks')), ('months', _('Months')), ('years', _('Years'))], default='days', verbose_name=_("Duration Unit"))
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_("Discount"))
    discount_start_date = models.DateField(blank=True, null=True, verbose_name=_("Discount Start Date"))
    discount_end_date = models.DateField(blank=True, null=True, verbose_name=_("Discount End Date"))
    additional_materials = models.ManyToManyField(AdditionalMaterial, related_name='included_in_packages', blank=True, verbose_name=_("Additional Materials"))
    lessons = models.ManyToManyField(Lesson, related_name='included_in_packages', blank=True, verbose_name=_("Lessons"))
    is_lifetime = models.BooleanField(default=False, verbose_name=_("Is Lifetime"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
