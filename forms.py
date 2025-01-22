from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth.forms import PasswordChangeForm

from .models import Profile
from django.forms.models import ModelForm

from django.forms.widgets import FileInput,PasswordInput

class ProfileForm(ModelForm):
    class Meta:
        model =Profile
        fields ='__all__'
        exclude = ['user']
        widgets ={
            'image':FileInput(),
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model =User
        fields=['username','email','password1','password2']
        widgets ={

            'password1':PasswordInput()
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))