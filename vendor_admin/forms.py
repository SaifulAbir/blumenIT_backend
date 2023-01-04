from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'User Name','class': 'form-control',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Input Password',
                                                                  'class': 'form-control','data-toggle': 'password','id': 'password'}))