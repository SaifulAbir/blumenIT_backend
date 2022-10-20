from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view()),
    path('checkout-details/<int:oid>/', CheckoutDetailsAPIView.as_view()),
    path('payment-methods/', PaymentMethodsAPIView.as_view()),
    path('apply-coupon/<str:code>/<int:uid>/', ApplyCouponAPIView.as_view()),
    # path('apply-coupon/', ApplyCouponAPIView.as_view()),
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

    # urmi
    path('create-billing-address/', BillingAddressCreateAPIView.as_view()),
    path('update-billing-address/<int:id>/',
         BillingAddressUpdateAPIView.as_view()),
    path('billing-address-list/', BillingAddressListAPIView.as_view()),
    path('delete-billing-address/<int:id>/',
         BillingAddressDeleteAPIView.as_view()),
    path('user-order-list/', UserOrderListAPIView.as_view()),
    # path('vendor-order-list/', VendorOrderListAPIView.as_view()),
    path('user-order-detail/<int:id>/', UserOrderDetailAPIView.as_view()),

]

#     path('vendor-order-detail/<int:pk>/', VendorOrderDetailsAPIView.as_view()),
