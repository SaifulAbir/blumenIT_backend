from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from vendor.models import Vendor
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect



class VendorLogin(SuccessMessageMixin ,LoginView):
    template_name = 'login.html'
    success_message = 'Successfully Logged In!'


class ForgotPassword(View):
    initial = {'key': 'value'}
    template_name = 'forgot-password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DashboardView(View):
    template_name = 'dashboard.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
