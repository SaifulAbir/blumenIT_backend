from django.urls import path
from .views import *

urlpatterns = [
    path('shipping-class-data/<str:country_id>/',
         ShippingClassDataAPIView.as_view()),
    path('checkout/', CheckoutAPIView.as_view()),
    path('checkout-details/<str:o_id>/', CheckoutDetailsAPIView.as_view()),
    path('apply-coupon/<str:code>/<int:uid>/', ApplyCouponAPIView.as_view()),
    path('discount-type-create/', DiscountTypeCreateAPIView.as_view()),
    path('discount-type-list/', DiscountTypeListAPI.as_view()),
    path('payment-types-list/', PaymentMethodsAPIView.as_view()),
    path('create-delivery-address/', DeliveryAddressCreateAPIView.as_view()),
    path('update-delivery-address/<int:id>/',
         DeliveryAddressUpdateAPIView.as_view()),
    path('delivery-address-list/', DeliveryAddressListAPIView.as_view()),
    path('delete-delivery-address/<int:id>/',
         DeliveryAddressDeleteAPIView.as_view()),
    path('wishlist-add-remove/<int:product_id>/',
         WishlistAddRemoveAPIView.as_view()),
    path('shipping-country-list/', ShippingCountryListAPIView.as_view()),
]
