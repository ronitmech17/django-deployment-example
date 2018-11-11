from django import forms
from . import models
from django.contrib.auth.models import User

class createNewUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')
