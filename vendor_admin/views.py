from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from vendor.models import Vendor
from .forms import VendorRequestForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# class VendorLogin(View):
# # def login(request):
# #     return render(request, 'login.html')

#     # form_class = InvestorRegisterForm
#     initial = {'key': 'value'}
#     template_name = 'login.html'

#     def get(self, request, *args, **kwargs):
#         # form = self.form_class(initial=self.initial)
#         # return render(request, self.template_name, {'form': form})
#         return render(request, self.template_name)

class VendorLogin(SuccessMessageMixin ,LoginView):
    template_name = 'login.html'
    success_message = 'Successfully Logged In!'

class VendorRequestView(View):
    form_class = VendorRequestForm
    initial = {'key': 'value'}
    template_name = 'request.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        # form = self.form_class(request.POST)
        # form = VendorRequestForm(request.POST)
        email = request.POST.get('email')
        organization_name = request.POST.get('organization_name')
        if email:
            User = get_user_model()
            if User.objects.filter(email = email).exists():
                messages.error(request, 'Email already in use!')
                return redirect(to='request')
            if Vendor.objects.filter(organization_name = organization_name).exists():
                messages.error(request, 'Organization name already in use!')
                return redirect(to='request')

            if form.is_valid():
                form.save()
                messages.success(request, 'Your request submitted successfully.')
                return redirect(to='login')
            else:
                messages.error(request, 'Form data not valid!')
                return redirect(to='request')
        



class ForgotPassword(View):
# def forgot_password(request):
#     return render(request, 'forgot-password.html')

    # form_class = InvestorRegisterForm
    initial = {'key': 'value'}
    template_name = 'forgot-password.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return render(request, self.template_name)

class DashboardView(View):
    template_name = 'dashboard.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
