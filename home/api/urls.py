from django.urls import path
from .views import *

urlpatterns = [
    path('home-data/', HomeDataAPIView.as_view()),
    path('contact-us/', ContactUsAPIView.as_view()),
    path('faq/', CreateGetFaqAPIView.as_view()),
    path('product-list-for-home-compare/',
         ProductListHomeCompareAPIView.as_view()),
    path('request-quote/', RequestQuoteAPIView.as_view()),

    path('gaming-data/', GamingDataAPIView.as_view()),
    path('create-corporate-deal/', CorporateDealCreateAPIView.as_view()),
    path('single-row-data/', SingleRowDataAPIView.as_view()),


    # pages
    path('admin/pages-list/', PagesListAPIView.as_view()),
    path('admin/pages-create/', PagesCreateAPIView.as_view()),
    path('admin/pages-update/<int:id>/', PagesUpdateAPIView.as_view()),
]
