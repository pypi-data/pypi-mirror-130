
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.forms import fields
from tkm.models import *

class CustomerRegisterationsForm(UserCreationForm):
    password1 =forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 =forms.CharField(label='Confirm',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    username =forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class LoginForm(AuthenticationForm):
    username =forms.CharField(label='Username',widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password =forms.CharField(label='password',widget=forms.PasswordInput(attrs={'autocomplete':'current','class':'form-control'}))
 

class PostForm(forms.ModelForm):
    title=forms.CharField(label='Title',widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    text=forms.CharField(label='Description',widget=forms.Textarea(attrs={'autofocus':True,'class':'form-control he'}))
   
    class Meta:
        model=Post
        fields = ['title','text','image']

        
