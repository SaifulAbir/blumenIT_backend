from django.urls import path
from .views import *

urlpatterns = [
    path('add-to-cart/<str:slug>/', AddToCartAPIView.as_view()),
    path('remove-from-cart/<str:slug>/', RemoveFromCartAPIView.as_view()),
    path('remove-item-from-cart/<str:slug>/', RemoveSingleItemFromCartAPIView.as_view()),
    path('cart-list/<int:uid>/', CartList.as_view()),
]