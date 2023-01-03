from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view()),
    path('checkout-details/<str:o_id>/', CheckoutDetailsAPIView.as_view()),

    path('coupon-create/', CouponCreateAPIView.as_view()),
    path('coupon-list/', CouponListAPIView.as_view()),
    path('coupon-update/<int:id>/', CouponUpdateAPIView.as_view()),
    path('apply-coupon/<str:code>/<int:uid>/', ApplyCouponAPIView.as_view()),
    path('discount-type-create/', DiscountTypeCreateAPIView.as_view()),
    path('discount-type-list/', DiscountTypeListAPI.as_view()),
    path('payment-types-list/', PaymentMethodsAPIView.as_view()),

    # urmi
    path('create-delivery-address/', DeliveryAddressCreateAPIView.as_view()),
    path('update-delivery-address/<int:id>/', DeliveryAddressUpdateAPIView.as_view()),
    path('delivery-address-list/', DeliveryAddressListAPIView.as_view()),
    path('delete-delivery-address/<int:id>/', BillingAddressDeleteAPIView.as_view()),

    path('wishlist-add-remove/<int:product_id>/', WishlistAddRemoveAPIView.as_view()),

    # path('create-payment-type/', PaymentTypeCreateAPIView.as_view()),
    # path('checkout-details/<int:oid>/', CheckoutDetailsAPIView.as_view()),
#     path('apply-coupon/<str:code>/<int:uid>/', ApplyCouponAPIView.as_view()),
    # path('apply-coupon/', ApplyCouponAPIView.as_view()),
#     path('user-order-list/', UserOrderListAPIView.as_view()),
    # path('vendor-order-list/', VendorOrderListAPIView.as_view()),
#     path('user-order-detail/<int:id>/', UserOrderDetailAPIView.as_view()),
#     path('vendor-order-detail/<int:pk>/', VendorOrderDetailsAPIView.as_view()),

]


