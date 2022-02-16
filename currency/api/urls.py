from django.urls import path
from .views import *

urlpatterns = [
    path('currency-list/', CurrencyListAPI.as_view()),
]