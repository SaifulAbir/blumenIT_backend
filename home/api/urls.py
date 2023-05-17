from django.urls import path
from .views import *

urlpatterns = [
    path('home-data/', HomeDataAPIView.as_view()),
    path('contact-us/', ContactUsAPIView.as_view()),
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

    # media
    path('admin/media-list/', MediaListAPIView.as_view()),
    path('admin/media-create/', MediaCreateAPIView.as_view()),
    path('admin/media-update/<int:id>/', MediaUpdateAPIView.as_view()),

    # faq
    path('admin/faq-list/', AdminFaqListAPIView.as_view()),
    path('admin/faq-create/', AdminFaqCreateAPIView.as_view()),
    path('admin/faq-update/<int:id>/', AdminFaqUpdateAPIView.as_view()),
    path('admin/faq-delete/<int:id>/', AdminFaqDeleteAPIView.as_view()),
]
