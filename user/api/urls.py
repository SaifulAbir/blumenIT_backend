from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from user.api.views import LoginUser, VerifyUserAPIView,  \
    SubscriptionAPIView,  ChangePasswordView, SendOTPAPIView, OTPVerifyAPIVIEW, ReSendOTPAPIView, \
    SetPasswordAPIView, SuperUserLoginUser, CustomerOrdersList, CustomerOrderDetails, CustomerProfile, CustomerAddressListAPIView, \
         CustomerAddressAddAPIView, CustomerAddressUpdateAPIView, CustomerAddressDeleteAPIView, DashboardDataAPIView, WishlistDataAPIView

urlpatterns = [
    path('login/', LoginUser.as_view({'post': 'create'}), name='login_user'),
    path('super-user-login/', SuperUserLoginUser.as_view({'post': 'create'}), name='super_user_login_user'),
    path('send-otp/', SendOTPAPIView.as_view(), name='send_otp'),
    path('otp-verify/', OTPVerifyAPIVIEW.as_view(), name='verify_otp'),
    path('resend-otp/', ReSendOTPAPIView.as_view(), name='resend_otp'),
    path('set-password/', SetPasswordAPIView.as_view(), name='set_password'),
    path('subscription/', SubscriptionAPIView.as_view()),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),

    path('customer/orders-list/', CustomerOrdersList.as_view()),
    path('customer/order-details/<str:o_id>/', CustomerOrderDetails.as_view()),
    path('customer/profile/<int:id>/', CustomerProfile.as_view()),
    path('customer/address-list/', CustomerAddressListAPIView.as_view()),
    path('customer/address-add/', CustomerAddressAddAPIView.as_view()),
    path('customer/address-update/<int:id>/', CustomerAddressUpdateAPIView.as_view()),
    path('customer/address-delete/<int:id>/', CustomerAddressDeleteAPIView.as_view()),
    path('customer/dashboard-data/', DashboardDataAPIView.as_view()),
    path('customer/wishlist-data/', WishlistDataAPIView.as_view()),

    # path('user-list/', UserListAPIView.as_view()),
    # path('change-password/', change_password),
    # path('verify-user/<str:verification_token>', VerifyUserAPIView.as_view()),
    # path('customer-profile/', CustomerRetrieveUpdateAPIView.as_view()),
    # path('customer-profile/update/', CustomerRetrieveUpdateAPIView.as_view()),
    # path('register-user/', csrf_exempt(RegisterUser.as_view({'post': 'create'})), name='register_user'),
]