from django import forms
from .models import UserRegistration


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['name', 'email', 'contact', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
