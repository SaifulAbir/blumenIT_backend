from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from vendor.models import VendorRequest
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django.utils.safestring import mark_safe

class VendorRegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': "Email",'class':'form-control'}))
    organization_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Organization Name','class': 'form-control',}))
    first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control',}))
    VENDOR_STATUSES =(
        ("Organization", "ORGANIZATION"),
        ("Individual", "INDIVIDUAL"),
    )
    vendor_status = forms.ChoiceField(choices = VENDOR_STATUSES,required=True,widget=forms.Select(attrs={'class': 'form-control',}))
    nid = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'NID', 'class': 'form-control', }))
    trade_license= forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'placeholder': 'Trade License'}))



    # name_of_company = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Name Of Startup','class': 'form-control',}))
    # web_link = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'placeholder': "Website / App Link",'class':'form-control'}))
    # sector_focus =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': "Sector Focus",'class':'form-control'}))
    
    # password = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Input Password',
    #                                                               'class': 'form-control','data-toggle': 'password','id': 'password'}))
    # company_phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Startup Phone', 'class': 'form-control'}))
    # company_linkedin_url = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'placeholder': 'Startup Linkedin URL', 'class': 'form-control'}))
    # STAGE_CHOICES =(
    #     ("pre_seed", "Pre Seed"),
    #     ("seed", "Seed"),
    # )
    # stage = forms.ChoiceField(choices = STAGE_CHOICES,required=True,widget=forms.Select(attrs={'class': 'form-control',}))
    # traction = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Traction', 'style':'background-color: #f5f6fa;'}))
    # link_for_pitch_deck = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'placeholder': 'Link For Pitch URL', 'class': 'form-control'}))
    # data_room = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': False}))
    # ban_im = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': False}))
    # iin = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': False}))
    # logo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    # title = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Project Title', 'class': 'form-control', }))
    # feature_image= forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    # amount = forms.DecimalField(max_digits=12, required=True,widget=forms.NumberInput(attrs={'placeholder': 'amount', 'class': 'form-control', }))

    class Meta: 
        model = VendorRequest
        fields = ['email', 'organization_name', 'first_name', 'last_name', 'vendor_status', 'nid' ]