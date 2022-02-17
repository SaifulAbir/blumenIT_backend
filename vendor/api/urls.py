from django.urls import path
from vendor.api.views import VendorRequestAPIView

urlpatterns = [
    path('vendor-request/', VendorRequestAPIView.as_view()),
]