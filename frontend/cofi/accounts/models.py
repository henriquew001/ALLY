from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUser(AbstractUser):
    # Remove username field
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": "A user with that username already exists.",
        },
        validators=[validate_email] #validate if it is a email address
    )
    email = models.EmailField("email address", blank=False)
    
    def clean(self):
        """
        Ensure that the username and email fields contain a valid email address.
        """
        try:
          validate_email(self.username)
        except ValidationError:
          raise ValidationError({"username":"The username has to be a valid email address."})
        return super().clean()
    
    def __str__(self):
        return self.email
