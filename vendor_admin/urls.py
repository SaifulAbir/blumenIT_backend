from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import VendorLogin, VendorRequestView, ForgotPassword, DashboardView
from vendor_admin.forms import UserLoginForm
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', VendorLogin.as_view(authentication_form=UserLoginForm), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('request/', VendorRequestView.as_view(), name='request'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]