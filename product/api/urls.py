from django.urls import path
from .views import *

urlpatterns = [
    path('create-product/', ProductCreateAPIView.as_view()),
]