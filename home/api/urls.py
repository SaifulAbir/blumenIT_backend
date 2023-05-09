from django.urls import path
from .views import *

urlpatterns = [
    path('home-data/', HomeDataAPIView.as_view()),
    path('contact-us/', ContactUsAPIView.as_view()),
    path('faq/', CreateGetFaqAPIView.as_view()),
    path('product-list-for-home-compare/',
         ProductListHomeCompareAPIView.as_view()),
    path('request-quote/', RequestQuoteAPIView.as_view()),

    path('gaming-data/', GamingDataAPIView.as_view()),
    path('create-corporate-deal/', CorporateDealCreateAPIView.as_view()),
    path('single-row-data/', SingleRowDataAPIView.as_view()),

    path('about-us-data/', AboutUsDataAPIView.as_view()),
    path('terms-and-condition-data/', TermsAndConditionDataAPIView.as_view()),
    path('online-service-support-data/',
         OnlineServiceSupportDataAPIView.as_view()),
    path('payment-method-data/', PaymentMethodDataAPIView.as_view()),
    path('refund-and-return-policy-data/',
         RefundAndReturnPolicyDataAPIView.as_view()),
    path('shipping-data/', ShippingDataAPIView.as_view()),
    path('privacy-policy-data/', PrivacyPolicyDataAPIView.as_view()),
    path('service-center-data/', ServiceCenterDataAPIView.as_view()),

    path('admin/about-us-list/', AboutUsListAPIView.as_view()),
    path('admin/terms-and-condition-list/',
         TermsAndConditionListAPIView.as_view()),
    path('admin/online-service-support-list/',
         OnlineServiceSupportListAPIView.as_view()),
    path('admin/payment-method-list/', PaymentMethodListAPIView.as_view()),
    path('admin/refund-and-return-policy-list/',
         RefundAndReturnPolicyListAPIView.as_view()),
    path('admin/shipping-list/', ShippingListAPIView.as_view()),
    path('admin/privacy-policy-list/', PrivacyPolicyListAPIView.as_view()),
    path('admin/service-center-list/', ServiceCenterListAPIView.as_view()),

    path('admin/about-us-create/', AboutUsCreateAPIView.as_view()),
    path('admin/terms-and-condition-create/',
         TermsAndConditionCreateAPIView.as_view()),
    path('admin/online-service-support-create/',
         OnlineServiceSupportCreateAPIView.as_view()),
    path('admin/payment-method-create/', PaymentMethodCreateAPIView.as_view()),
    path('admin/refund-and-return-policy-create/',
         RefundAndReturnPolicyCreateAPIView.as_view()),
    path('admin/shipping-create/', ShippingCreateAPIView.as_view()),
    path('admin/privacy-policy-create/', PrivacyPolicyCreateAPIView.as_view()),
    path('admin/service-center-create/', ServiceCenterCreateAPIView.as_view()),

    path('admin/about-us-update/<int:id>/', AboutUsUpdateAPIView.as_view()),
    path('admin/terms-and-condition-update/<int:id>/',
         TermsAndConditionUpdateAPIView.as_view()),
    path('admin/online-service-support-update/<int:id>/',
         OnlineServiceSupportUpdateAPIView.as_view()),
    path('admin/payment-method-update/<int:id>/',
         PaymentMethodUpdateAPIView.as_view()),
    path('admin/refund-and-return-policy-update/<int:id>/',
         RefundAndReturnPolicyUpdateAPIView.as_view()),
    path('admin/shipping-update/<int:id>/', ShippingUpdateAPIView.as_view()),
    path('admin/privacy-policy-update/<int:id>/',
         PrivacyPolicyUpdateAPIView.as_view()),
    path('admin/service-center-update/<int:id>/',
         ServiceCenterUpdateAPIView.as_view()),

    # path('gaming-category-list/', GamingCategoryListAPIView.as_view()),
    # path('product-list-by-category-gaming-popular-products/<int:id>/<str:type>/<int:pagination>/',
    #       ProductListByCategoryGamingPopularProductsAPI.as_view()),
    # path('gaming-featured-product-list/<int:pagination>/', GamingFeaturedProductListAPI.as_view()),
]
