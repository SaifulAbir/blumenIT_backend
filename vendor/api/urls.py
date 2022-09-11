from django.urls import path
from vendor.api.views import VendorAttributeListAPIView, VendorBrandListAPIView, VendorCategoryListAPIView, VendorRequestAPIView, VendorRequestListAPI, VendorCreateAPIView, \
    OrganizationNamesListAPIView, VendorDetailAPIView, StoreSettingsUpdateAPIView, VendorSubCategoryListAPIView, VendorSubSubCategoryListAPIView, VendorTagListAPIView, VendorUnitListAPIView, VendorProductListAPI, VendorProductCreateAPIView, VendorDiscountListAPIView, VendorVariantListAPIView

urlpatterns = [
    path('vendor-request/', VendorRequestAPIView.as_view()),
    path('vendor-request-list/', VendorRequestListAPI.as_view()),
    path('create-vendor/', VendorCreateAPIView.as_view()),
    path('organization-list/', OrganizationNamesListAPIView.as_view()),
    path('vendor-profile/', VendorDetailAPIView.as_view()),
    path('vendor-store-settings-update/', StoreSettingsUpdateAPIView.as_view()),
    path('vendor-product-category-list/', VendorCategoryListAPIView.as_view()),
    path('vendor-product-sub-category-list/<int:cid>/',
         VendorSubCategoryListAPIView.as_view()),
    path('vendor-product-sub-sub-category-list/<int:sid>/',
         VendorSubSubCategoryListAPIView.as_view()),
    path('vendor-product-brand-list/', VendorBrandListAPIView.as_view()),
    path('vendor-product-unit-list/', VendorUnitListAPIView.as_view()),
    path('vendor-product-discount-list/', VendorDiscountListAPIView.as_view()),
    path('vendor-product-tag-list/', VendorTagListAPIView.as_view()),
    path('vendor-product-attribute-list/',
         VendorAttributeListAPIView.as_view()),
    path('vendor-product-variant-list/', VendorVariantListAPIView.as_view()),
    path('vendor-product-list/', VendorProductListAPI.as_view()),
    path('vendor-create-product/', VendorProductCreateAPIView.as_view()),
    #     path('vendor-update-product/<str:slug>/',
    #          VendorProductUpdateAPIView.as_view()),
]
