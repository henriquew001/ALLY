from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
      'placeholder': 'Confirm Password'
      }))

  class Meta:
      model = CustomUser
      fields = ('email','password','password2')

  def clean(self):
      cleaned_data = super().clean()
      password = cleaned_data.get('password')
      password2 = cleaned_data.get('password2')

      if password != password2:
          raise forms.ValidationError("Passwords do not match")

      return cleaned_data
