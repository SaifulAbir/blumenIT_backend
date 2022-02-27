from django.urls import path
from vendor.api.views import VendorRequestAPIView, VendorRequestListAPI, VendorCreateAPIView

urlpatterns = [
    path('vendor-request/', VendorRequestAPIView.as_view()),
    path('vendor-request-list/', VendorRequestListAPI.as_view()),
    path('create-vendor/', VendorCreateAPIView.as_view()),
]