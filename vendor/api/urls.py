from django.urls import path
from vendor.api.views import VendorRequestAPIView, VendorRequestListAPI, VendorCreateAPIView, \
    OrganizationNamesListAPIView, VendorDetailAPIView, StoreSettingsUpdateAPIView

urlpatterns = [
    path('vendor-request/', VendorRequestAPIView.as_view()),
    path('vendor-request-list/', VendorRequestListAPI.as_view()),
    path('create-vendor/', VendorCreateAPIView.as_view()),
    path('organization-list/', OrganizationNamesListAPIView.as_view()),
    path('vendor-profile/', VendorDetailAPIView.as_view()),
    path('vendor-store-settings-update/', StoreSettingsUpdateAPIView.as_view()),
]