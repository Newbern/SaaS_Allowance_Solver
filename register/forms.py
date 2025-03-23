from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={"class": "test"}),
            'email': forms.TextInput(attrs={"class": "test"}),
            'password1': forms.PasswordInput(attrs={"class": "test"}),
            'password2': forms.PasswordInput(attrs={"class": "test"})
        }
