# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Hello, world. You're at the admin lte index.")

from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def forgot_password(request):
    return render(request, 'forgot-password.html')