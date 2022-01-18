from django.urls import path
from .views import *

urlpatterns = [
    path('create-product/', ProductCreateAPIView.as_view()),
    path('product-list/', ProductListAPI.as_view()),
    path('tags-list/', TagsListAPI.as_view()),
    path('update-product/<str:slug>/', ProductUpdateAPIView.as_view()),
    path('create-tag/', TagCreateAPIView.as_view()),
]