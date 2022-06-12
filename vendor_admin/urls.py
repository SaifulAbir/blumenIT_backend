from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import VendorLogin, VendorRegisterView, ForgotPassword

urlpatterns = [
    path('login/', VendorLogin.as_view(), name='login'),
    path('register/', VendorRegisterView.as_view(), name='register'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
]