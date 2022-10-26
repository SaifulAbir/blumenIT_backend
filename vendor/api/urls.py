from django.urls import path
from product.api.views import ProductDetailsAPI
from vendor.api.views import VendorAddNewCategoryAPIView, VendorAddNewSubCategoryAPIView, VendorAddNewSubSubCategoryAPIView, VendorBrandListAPIView, VendorCategoryListAPIView, VendorDeleteCategoryAPIView, VendorDeleteSubCategoryAPIView, VendorDeleteSubSubCategoryAPIView, VendorProductDeleteAPI, VendorProductUpdateAPIView, VendorProductViewAPI, VendorSubCategoryListAPIView, VendorSubSubCategoryListAPIView, VendorTagListAPIView, VendorUnitListAPIView, VendorProductListAPI, VendorProductCreateAPIView, VendorDiscountListAPIView, SellerCreateAPIView,SellerListAPIView,SellerUpdateAPIView, SellerDeleteAPIView, VendorUpdateCategoryAPIView, VendorUpdateSubCategoryAPIView, VendorUpdateSubSubCategoryAPIView, VendorVatTypeListAPIView, VendorVideoProviderListAPIView

urlpatterns = [
    path('create-seller/', SellerCreateAPIView.as_view()),
    path('seller-list/', SellerListAPIView.as_view()),
    path('seller-update/<int:id>/', SellerUpdateAPIView.as_view()),
    path('seller-delete/<int:id>/', SellerDeleteAPIView.as_view()),
    # path('vendor-request/', VendorRequestAPIView.as_view()),
    # path('vendor-request-list/', VendorRequestListAPI.as_view()),
    # path('create-vendor/', VendorCreateAPIView.as_view()),
    # # path('update-vendor/', VendorUpdateAPIView.as_view())
    # path('organization-list/', OrganizationNamesListAPIView.as_view()),
    # path('vendor-profile/', VendorDetailAPIView.as_view()),
    # path('vendor-store-settings-update/', StoreSettingsUpdateAPIView.as_view()),
    path('vendor-product-category-list/', VendorCategoryListAPIView.as_view()),
    path('vendor-add-new-category/', VendorAddNewCategoryAPIView.as_view()),
    path('vendor-update-category/<int:ordering_number>/', VendorUpdateCategoryAPIView.as_view()),
    path('vendor-delete-category/<int:ordering_number>/', VendorDeleteCategoryAPIView.as_view()),

    path('vendor-product-sub-category-list/<int:cid>/',VendorSubSubCategoryListAPIView.as_view()),
    path('vendor-add-new-sub-category/', VendorAddNewSubCategoryAPIView.as_view()),
    path('vendor-update-sub-category/<int:ordering_number>/', VendorUpdateSubCategoryAPIView.as_view()),
    path('vendor-delete-sub-category/<int:ordering_number>/', VendorDeleteSubCategoryAPIView.as_view()),

    path('vendor-product-sub-sub-category-list/<int:sid>/',VendorSubSubCategoryListAPIView.as_view()),
    path('vendor-add-new-sub-sub-category/', VendorAddNewSubSubCategoryAPIView.as_view()),
    path('vendor-update-sub-sub-category/<int:ordering_number>/', VendorUpdateSubSubCategoryAPIView.as_view()),
    path('vendor-delete-sub-sub-category/<int:ordering_number>/', VendorDeleteSubSubCategoryAPIView.as_view()),

    path('vendor-product-brand-list/', VendorBrandListAPIView.as_view()),
    path('vendor-product-unit-list/', VendorUnitListAPIView.as_view()),
    path('vendor-product-discount-list/', VendorDiscountListAPIView.as_view()),
    path('vendor-product-tag-list/', VendorTagListAPIView.as_view()),
    path('vendor-product-video-provider-list/', VendorVideoProviderListAPIView.as_view()),
    path('vendor-product-vat-type-list/', VendorVatTypeListAPIView.as_view()),
    # path('vendor-product-attribute-list/',
    #      VendorAttributeListAPIView.as_view()),
    # path('vendor-product-variant-list/', VendorVariantListAPIView.as_view()),
    path('vendor-product-list/', VendorProductListAPI.as_view()),
    path('vendor-create-product/', VendorProductCreateAPIView.as_view()),
    path('vendor-update-product/<str:slug>/',
         VendorProductUpdateAPIView.as_view()),
#     path('vendor-product-details/<str:slugi>/',
#          VendorProductDetailsAPI.as_view()),
    # path('vendor-product-single-media-delete/<str:slug>/<int:mid>/',
    #      VendorProductSingleMediaDeleteAPI.as_view()),
    path('vendor-product-delete/<str:slug>/',
         VendorProductDeleteAPI.as_view()),
    path('vendor-product-view/<str:slugi>/',
         VendorProductViewAPI.as_view()),

]
