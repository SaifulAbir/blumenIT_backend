from django.urls import path
from .views import *

urlpatterns = [
    path('home-data/', HomeDataAPIView.as_view()),
    path('contact-us/', ContactUsAPIView.as_view()),
    path('faq/', CreateGetFaqAPIView.as_view()),
    # path('recent-view/', RecentAPIView.as_view()),
]