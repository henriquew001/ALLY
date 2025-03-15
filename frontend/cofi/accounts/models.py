from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Füge hier zusätzliche Felder hinzu, falls benötigt
    # Beispiel:
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username
