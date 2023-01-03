from django import forms
from vendor.models import VendorRequest
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import AuthenticationForm

class VendorRequestForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': "Email",'class':'form-control'}))
    organization_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Organization Name','class': 'form-control',}))
    first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control',}))
    VENDOR_TYPES =(
        ("Organization", "ORGANIZATION"),
        ("Individual", "INDIVIDUAL"),
    )
    vendor_type = forms.ChoiceField(
        choices = VENDOR_TYPES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control',}))
    nid = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'NID', 'class': 'form-control', }))
    trade_license= forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'placeholder': 'Trade License'}))

    class Meta:
        model = VendorRequest
        fields = ['email', 'organization_name', 'first_name', 'last_name', 'vendor_type', 'nid', 'trade_license' ]

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'User Name','class': 'form-control',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Input Password',
                                                                  'class': 'form-control','data-toggle': 'password','id': 'password'}))