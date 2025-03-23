from django.db import models
from django.conf import settings

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_example = models.BooleanField(default=False)

    def __str__(self):
        return self.title

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
    description = models.TextField()
    is_recurring = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # Add other fields like duration, etc.
    additional_materials = models.ManyToManyField(AdditionalMaterial, related_name='included_in_packages', blank=True)

    def __str__(self):
        return self.name

class UserPackage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"
