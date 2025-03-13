# /home/heinrich/projects/ConsciousFit/frontend/django/accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings # import settings

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        label=_("Password"),
        help_text=_("Enter a strong password."),
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        label=_("Confirm Password"),
        help_text=_("Confirm the password."),
    )
    email = forms.EmailField(required=True, label=_("Email")) #added this

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': '',
            'email': _('Required') # added this
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.fields['username'].help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        email = cleaned_data.get("email")

        if password and password_confirm and password != password_confirm:
            self.add_error("password", forms.ValidationError(_("Passwords do not match.")))
        if email:
            if User.objects.filter(email=email).exists():
                self.add_error("email", forms.ValidationError(_("This email address is already in use.")))

        # Enforce the password validators
        errors = list()
        for validator in settings.AUTH_PASSWORD_VALIDATORS: #iterate through the validators in settings
            # import the validator-class
            validator_class = getattr(
                __import__(".".join(validator['NAME'].split(".")[:-1]), fromlist=['']),
                validator['NAME'].split(".")[-1]
                )
            validator_instance = validator_class() #create an instance
            try:
                validator_instance.validate(password, User) # check if the password is valid
            except ValidationError as e:
                errors.extend(list(e.messages)) #if there are errors, add them to the list
        if errors:
            self.add_error("password", ValidationError(errors)) # add the errors to the password field

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
