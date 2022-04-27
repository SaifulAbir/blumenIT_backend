from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .forms import VendorRegisterForm

class VendorLogin(View):
# def login(request):
#     return render(request, 'login.html')

    # form_class = InvestorRegisterForm
    initial = {'key': 'value'}
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return render(request, self.template_name)

class VendorRegisterView(View):
    form_class = VendorRegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
        # return render(request, self.template_name)


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
