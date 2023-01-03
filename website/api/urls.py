from django.urls import path
from .views import *

urlpatterns = [
    path('header/', HeaderAPIView.as_view()),
]