from django.urls import path
from product.api.views import ProductDetailsAPI
from vendor.api.views import AdminAddNewSubCategoryAPIView, AdminAddNewSubSubCategoryAPIView, AdminBrandListAPIView,\
    AdminCategoryListAPIView, AdminDeleteCategoryAPIView, AdminDeleteSubCategoryAPIView, \
    AdminDeleteSubSubCategoryAPIView, AdminProductDeleteAPI, AdminProductViewAPI, AdminSubCategoryListAPIView,\
    AdminSubSubCategoryListAPIView, AdminTagListAPIView, AdminUnitListAPIView,\
    AdminDiscountListAPIView,\
    AdminUpdateCategoryAPIView, AdminUpdateSubCategoryAPIView, AdminUpdateSubSubCategoryAPIView, \
    AdminVatTypeListAPIView, AdminVideoProviderListAPIView, \
    AdminProductCreateAPIView, AdminCreateAPIView, AdminListAPIView, AdminUpdateAPIView, AdminDeleteAPIView,\
    AdminDetailsAPIView, AdminProductUpdateAPIView, AdminAddNewCategoryAPIView, AdminProductListAPI, AdminFlashDealCreateAPIView

urlpatterns = [
    path('admin/create/', AdminCreateAPIView.as_view()),
    path('admin/list/', AdminListAPIView.as_view()),
    path('admin/update/<int:id>/', AdminUpdateAPIView.as_view()),
    path('admin/delete/<int:id>/', AdminDeleteAPIView.as_view()),
    path('admin/details/<int:id>/', AdminDetailsAPIView.as_view()),

    path('admin/product-create/', AdminProductCreateAPIView.as_view()),
    path('admin/product-update/<str:slug>/',AdminProductUpdateAPIView.as_view()),
    path('admin/add-new-category/', AdminAddNewCategoryAPIView.as_view()),

    path('admin/product-list/', AdminProductListAPI.as_view()),

    path('admin/product-delete/<str:slug>/',AdminProductDeleteAPI.as_view()),
    path('admin/product-view/<str:slugi>/',AdminProductViewAPI.as_view()),

    path('admin/product-category-list/', AdminCategoryListAPIView.as_view()),
    path('admin/update-category/<int:ordering_number>/', AdminUpdateCategoryAPIView.as_view()),
    path('admin/delete-category/<int:ordering_number>/', AdminDeleteCategoryAPIView.as_view()),

    path('admin/product-sub-category-list/<int:cid>/',AdminSubCategoryListAPIView.as_view()),
    path('admin/add-new-sub-category/', AdminAddNewSubCategoryAPIView.as_view()),
    path('admin/update-sub-category/<int:ordering_number>/', AdminUpdateSubCategoryAPIView.as_view()),
    path('admin/delete-sub-category/<int:ordering_number>/', AdminDeleteSubCategoryAPIView.as_view()),

    path('admin/product-sub-sub-category-list/<int:sid>/',AdminSubSubCategoryListAPIView.as_view()),
    path('admin/add-new-sub-sub-category/', AdminAddNewSubSubCategoryAPIView.as_view()),
    path('admin/update-sub-sub-category/<int:ordering_number>/', AdminUpdateSubSubCategoryAPIView.as_view()),
    path('admin/delete-sub-sub-category/<int:ordering_number>/', AdminDeleteSubSubCategoryAPIView.as_view()),

    path('admin/product-brand-list/', AdminBrandListAPIView.as_view()),
    path('admin/product-unit-list/', AdminUnitListAPIView.as_view()),
    path('admin/product-discount-list/', AdminDiscountListAPIView.as_view()),
    path('admin/product-tag-list/', AdminTagListAPIView.as_view()),
    path('admin/product-video-provider-list/', AdminVideoProviderListAPIView.as_view()),
    path('admin/product-vat-type-list/', AdminVatTypeListAPIView.as_view()),

    path('admin/flash-deal-create/', AdminFlashDealCreateAPIView.as_view()),


    # # path('update-vendor/', VendorUpdateAPIView.as_view()),
    # path('vendor-product-attribute-list/',
    #      VendorAttributeListAPIView.as_view()),
    # path('vendor-product-variant-list/', VendorVariantListAPIView.as_view()),

]
