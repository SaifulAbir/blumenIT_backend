from django.urls import path
from .views import *

urlpatterns = [
    path('create-product/', ProductCreateAPIView.as_view()),
    path('update-product/<str:slug>/', ProductUpdateAPIView.as_view()),
]