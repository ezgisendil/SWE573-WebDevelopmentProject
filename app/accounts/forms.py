from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields import CharField
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from service.models import Post
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']


#adding textfield in forms?????

#update username, email and shortbio
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']

#update profile picture
class ProfileUpdateForm(forms.ModelForm):
    location = forms.CharField()
    shortbio = forms.TextInput()
    interests = forms.CharField()
    class Meta:
        model = Profile
        fields = ['location', 'occupation', 'shortbio', 'interests', 'image']


