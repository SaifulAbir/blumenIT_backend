from django.urls import path
from vendor.api.views import VendorBrandListAPIView, VendorCategoryListAPIView, VendorRequestAPIView, VendorRequestListAPI, VendorCreateAPIView, \
    OrganizationNamesListAPIView, VendorDetailAPIView, StoreSettingsUpdateAPIView, VendorSubCategoryListAPIView, VendorSubSubCategoryListAPIView, VendorUnitListAPIView, VendorProductListAPI

urlpatterns = [
    path('vendor-request/', VendorRequestAPIView.as_view()),
    path('vendor-request-list/', VendorRequestListAPI.as_view()),
    path('create-vendor/', VendorCreateAPIView.as_view()),
    path('organization-list/', OrganizationNamesListAPIView.as_view()),
    path('vendor-profile/', VendorDetailAPIView.as_view()),
    path('vendor-store-settings-update/', StoreSettingsUpdateAPIView.as_view()),
    path('vendor-category-list/', VendorCategoryListAPIView.as_view()),
    path('vendor-sub-category-list/<int:cid>/', VendorSubCategoryListAPIView.as_view()),
    path('vendor-sub-sub-category-list/<int:cid>/', VendorSubSubCategoryListAPIView.as_view()),
    path('vendor-brand-list/', VendorBrandListAPIView.as_view()),
    path('vendor-unit-list/', VendorUnitListAPIView.as_view()),
    path('vendor-product-list/<int:vid>/', VendorProductListAPI.as_view()),
]
