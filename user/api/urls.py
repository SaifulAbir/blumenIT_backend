from django.urls import path
from user.api.views import LoginUser,  \
    SubscriptionAPIView,  ChangePasswordView, SendOTPAPIView, OTPVerifyAPIVIEW, ReSendOTPAPIView, \
    SetPasswordAPIView, SuperUserLoginUser, CustomerOrdersList, CustomerOrderDetails, CustomerProfile, CustomerAddressListAPIView, \
    CustomerAddressAddAPIView, CustomerAddressUpdateAPIView, CustomerAddressDeleteAPIView, DashboardDataAPIView, WishlistDataAPIView, \
    SavePcAPIView, SavePcListAPIView, SavePcViewAPIView, SavePcDeleteAPIView

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
    path('customer/save-pc/', SavePcAPIView.as_view()),
    path('customer/save-pc-list/', SavePcListAPIView.as_view()),
    path('customer/save-pc-view/<int:id>/', SavePcViewAPIView.as_view()),
    path('customer/save-pc-delete/<int:id>/', SavePcDeleteAPIView.as_view()),

]