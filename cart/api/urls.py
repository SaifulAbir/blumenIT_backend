from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view()),
    path('payment-methods/', PaymentMethodsAPIView.as_view()),
    path('apply-coupon/<str:code>/', ApplyCouponAPIView.as_view()),
    path('wishlist-data/', WishListAPIView.as_view()),
    path('destroy-wishlist-data/<int:id>/', WishlistDeleteAPIView.as_view()),

    # path('active-coupon/', ActiveCouponlistView.as_view()),
    # path('add-to-cart/<str:slug>/', AddToCartAPIView.as_view()),
    # path('remove-from-cart/<str:slug>/', RemoveFromCartAPIView.as_view()),
    # path('remove-item-from-cart/<str:slug>/', RemoveSingleItemFromCartAPIView.as_view()),
    # path('cart-list/<int:uid>/', CartList.as_view()),
    # path('create-payment-type/', PaymentTypeCreateAPIView.as_view()),
    # path('total-price/', TotalPriceAPIView.as_view()),
    # path('check-quantity/', CheckQuantityAPIView.as_view()),
]