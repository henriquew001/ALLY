# /home/heinrich/projects/ConsciousFit/frontend/cofi/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import timedelta

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Füge hier zusätzliche Felder hinzu, falls benötigt
    # Beispiel:
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    username = models.CharField(
        max_length=150,
        unique=False,  # Allow duplicate usernames
        blank=True, #allow empty usernames
        null=True  # Allow null usernames
    )
    email = models.EmailField(unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove 'email' and 'username' as it is now the USERNAME_FIELD and optional.

    objects = CustomUserManager() #add the new user manager

    def __str__(self):
        return self.email #we now use the email as identifier

    def clean(self):
        super().clean()
        if not self.email:
            raise ValidationError({'email': 'This field cannot be blank.'})

class UserPackage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey('cms.Package', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    next_payment_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.package.name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Nur beim ersten Erstellen
            if self.package.is_lifetime:
                self.end_date = None
            else:
                if self.package.duration is not None and self.package.duration_unit is not None:
                    if self.package.duration_unit == 'days':
                        self.end_date = self.start_date + timedelta(days=self.package.duration)
                    elif self.package.duration_unit == 'weeks':
                        self.end_date = self.start_date + timedelta(weeks=self.package.duration)
                    elif self.package.duration_unit == 'months':
                        self.end_date = self.start_date + timedelta(days=self.package.duration * 30)  # Ungef
