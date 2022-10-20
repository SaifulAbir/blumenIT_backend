from django.urls import path
from product.api.views import ProductDetailsAPI
from vendor.api.views import VendorAttributeListAPIView, VendorBrandListAPIView, VendorCategoryListAPIView, VendorProductDeleteAPI, VendorProductDetailsAPI, VendorProductSingleMediaDeleteAPI, VendorProductUpdateAPIView, VendorRequestAPIView, VendorRequestListAPI, VendorCreateAPIView, OrganizationNamesListAPIView, VendorDetailAPIView, StoreSettingsUpdateAPIView, VendorSubCategoryListAPIView, VendorSubSubCategoryListAPIView, VendorTagListAPIView, VendorUnitListAPIView, VendorProductListAPI, VendorProductCreateAPIView, VendorDiscountListAPIView, VendorVariantListAPIView,SellerCreateAPIView,SellerListAPIView,SellerUpdateAPIView, SellerDeleteAPIView

urlpatterns = [
    path('create-seller/', SellerCreateAPIView.as_view()),
    path('seller-list/', SellerListAPIView.as_view()),
    path('seller-update/<int:id>/', SellerUpdateAPIView.as_view()),
    path('seller-delete/<int:id>/', SellerDeleteAPIView.as_view()),
    path('coupon-create/', SellerCreateAPIView.as_view()),
    path('coupon-list/', SellerListAPIView.as_view()),
    path('coupon-update/<int:id>/', SellerUpdateAPIView.as_view()),
    # path('vendor-request/', VendorRequestAPIView.as_view()),
    # path('vendor-request-list/', VendorRequestListAPI.as_view()),
    # path('create-vendor/', VendorCreateAPIView.as_view()),
    # # path('update-vendor/', VendorUpdateAPIView.as_view())
    # path('organization-list/', OrganizationNamesListAPIView.as_view()),
    # path('vendor-profile/', VendorDetailAPIView.as_view()),
    # path('vendor-store-settings-update/', StoreSettingsUpdateAPIView.as_view()),
    # path('vendor-product-category-list/', VendorCategoryListAPIView.as_view()),
    # path('vendor-product-sub-category-list/<int:cid>/',
    #      VendorSubCategoryListAPIView.as_view()),
    # path('vendor-product-sub-sub-category-list/<int:sid>/',
    #      VendorSubSubCategoryListAPIView.as_view()),
    # path('vendor-product-brand-list/', VendorBrandListAPIView.as_view()),
    # path('vendor-product-unit-list/', VendorUnitListAPIView.as_view()),
    # path('vendor-product-discount-list/', VendorDiscountListAPIView.as_view()),
    # path('vendor-product-tag-list/', VendorTagListAPIView.as_view()),
    # path('vendor-product-attribute-list/',
    #      VendorAttributeListAPIView.as_view()),
    # path('vendor-product-variant-list/', VendorVariantListAPIView.as_view()),
    # path('vendor-product-list/', VendorProductListAPI.as_view()),
    # path('vendor-create-product/', VendorProductCreateAPIView.as_view()),
    # path('vendor-update-product/<str:slug>/',
    #      VendorProductUpdateAPIView.as_view()),
    # path('vendor-product-details/<str:slugi>/',
    #      VendorProductDetailsAPI.as_view()),
    # path('vendor-product-single-media-delete/<str:slug>/<int:mid>/',
    #      VendorProductSingleMediaDeleteAPI.as_view()),
    # path('vendor-product-delete/<str:slug>/',
    #      VendorProductDeleteAPI.as_view()),

]
