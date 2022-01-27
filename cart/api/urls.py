from django.urls import path
from .views import *

urlpatterns = [
    path('add-to-cart/<str:slug>/', AddToCartAPIView.as_view(), name='add-to-cart'),
]