from django.urls import path
from .views import *

urlpatterns = [
    path('create-product/', ProductCreateAPIView.as_view()),
    path('product-categories/', ProductCategoriesCreateAPI.as_view()),
    path('product-brands/', ProductBrandsCreateAPI.as_view()),
]