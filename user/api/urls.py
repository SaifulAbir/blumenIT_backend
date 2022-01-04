from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from user.api.views import RegisterUser, LoginUser

urlpatterns = [
    path('login/', LoginUser.as_view({'post': 'create'}), name='login_user'),
    path('register-user/', csrf_exempt(RegisterUser.as_view({'post': 'create'})), name='register_user'),
]