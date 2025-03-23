from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) #add the PasswordInput widget
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_active', 'is_staff', 'is_superuser') # Include all the fields you want to edit in the admin.
        # exclude = ('password',) # if you want to exclude password from the form