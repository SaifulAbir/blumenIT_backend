from django.urls import path
from .views import *

urlpatterns = [
    path('home-data/', HomeDataAPIView.as_view()),
    path('contact-us/', ContactUsAPIView.as_view()),
    path('faq/', CreateGetFaqAPIView.as_view()),
    path('product-list-for-home-compare/', ProductListHomeCompareAPIView.as_view()),
    path('request-quote/', RequestQuoteAPIView.as_view()),

    path('gaming-data/', GamingDataAPIView.as_view()),
    path('create-corporate-deal/', CorporateDealCreateAPIView.as_view()),

    # path('gaming-category-list/', GamingCategoryListAPIView.as_view()),
    # path('product-list-by-category-gaming-popular-products/<int:id>/<str:type>/<int:pagination>/',
    #       ProductListByCategoryGamingPopularProductsAPI.as_view()),
    # path('gaming-featured-product-list/<int:pagination>/', GamingFeaturedProductListAPI.as_view()),
]