from django.urls import path
from vendor.api.views import AdminAddNewSubCategoryAPIView, AdminAddNewSubSubCategoryAPIView, AdminBrandListAPIView,\
    AdminCategoryListAPIView, AdminDeleteCategoryAPIView, AdminDeleteSubCategoryAPIView, \
    AdminDeleteSubSubCategoryAPIView, AdminProductDeleteAPI, AdminProductViewAPI, AdminSubCategoryListAPIView,\
    AdminSubSubCategoryListAPIView, AdminTagListAPIView, AdminUnitListAPIView,\
    AdminDiscountListAPIView,\
    AdminUpdateCategoryAPIView, AdminUpdateSubCategoryAPIView, AdminUpdateSubSubCategoryAPIView, \
    AdminVatTypeListAPIView, AdminVideoProviderListAPIView, \
    AdminProductCreateAPIView, AdminSellerCreateAPIView, AdminSellerListAPIView, AdminSellerUpdateAPIView, AdminSellerDeleteAPIView,\
    AdminSellerDetailsAPIView, AdminProductUpdateAPIView, AdminAddNewCategoryAPIView, AdminProductListAPI, AdminFlashDealCreateAPIView,\
    AdminFilterAttributesAPI, AdminProfileAPIView, AdminReviewListAPIView, AdminReviewInactiveAPIView, ReviewSearchAPI, \
    AdminAttributeListAPIView, AdminAddNewAttributeAPIView, AdminUpdateAttributeAPIView, AdminAttributeValuesListAPIView, \
    AdminAddNewAttributeValueAPIView, AdminUpdateAttributeValueAPIView, AdminFilterAttributeListAPIView, AdminAddNewFilterAttributeAPIView, \
    AdminProductListSearchAPI, AdminOrderList, AdminOrderViewAPI, OrderListSearchAPI, AdminOrderUpdateAPI, \
    AdminUpdateFilterAttributeAPIView, AdminCustomerListAPIView, AdminTicketListAPIView, AdminTicketDetailsAPIView, \
    AdminUpdateTicketStatusAPIView, AdminDashboardDataAPIView, AdminBrandCreateAPIView, AdminBrandDeleteAPIView, \
    AdminFlashDealListAPIView

urlpatterns = [
    path('admin/seller-create/', AdminSellerCreateAPIView.as_view()),
    path('admin/seller-list/', AdminSellerListAPIView.as_view()),
    path('admin/seller-update/<int:id>/', AdminSellerUpdateAPIView.as_view()),
    path('admin/seller-delete/<int:id>/', AdminSellerDeleteAPIView.as_view()),
    path('admin/seller-details/<int:id>/', AdminSellerDetailsAPIView.as_view()),
    path('admin/product-create/', AdminProductCreateAPIView.as_view()),
    path('admin/product-update/<str:slug>/',AdminProductUpdateAPIView.as_view()),
    path('admin/product-list/', AdminProductListAPI.as_view()),
    path('admin/product-list-search/', AdminProductListSearchAPI.as_view()),
    path('admin/product-delete/<str:slug>/',AdminProductDeleteAPI.as_view()),
    path('admin/product-view/<str:slugi>/',AdminProductViewAPI.as_view()),
    path('admin/filtering-attributes/<int:id>/<str:type>/', AdminFilterAttributesAPI.as_view()),
    path('admin/category-list/', AdminCategoryListAPIView.as_view()),
    path('admin/add-new-category/', AdminAddNewCategoryAPIView.as_view()),
    path('admin/update-category/<int:id>/', AdminUpdateCategoryAPIView.as_view()),
    path('admin/delete-category/<int:id>/', AdminDeleteCategoryAPIView.as_view()),
    path('admin/sub-category-list/<int:cid>/',AdminSubCategoryListAPIView.as_view()),
    path('admin/add-new-sub-category/', AdminAddNewSubCategoryAPIView.as_view()),
    path('admin/update-sub-category/<int:id>/', AdminUpdateSubCategoryAPIView.as_view()),
    path('admin/delete-sub-category/<int:id>/', AdminDeleteSubCategoryAPIView.as_view()),
    path('admin/sub-sub-category-list/<int:sid>/',AdminSubSubCategoryListAPIView.as_view()),
    path('admin/add-new-sub-sub-category/', AdminAddNewSubSubCategoryAPIView.as_view()),
    path('admin/update-sub-sub-category/<int:id>/', AdminUpdateSubSubCategoryAPIView.as_view()),
    path('admin/delete-sub-sub-category/<int:id>/', AdminDeleteSubSubCategoryAPIView.as_view()),
    path('admin/brand-create/', AdminBrandCreateAPIView.as_view()),
    path('admin/brand-delete/<int:id>/', AdminBrandDeleteAPIView.as_view()),
    path('admin/product-brand-list/', AdminBrandListAPIView.as_view()),
    path('admin/product-unit-list/', AdminUnitListAPIView.as_view()),
    path('admin/product-discount-list/', AdminDiscountListAPIView.as_view()),
    path('admin/product-tag-list/', AdminTagListAPIView.as_view()),
    path('admin/product-video-provider-list/', AdminVideoProviderListAPIView.as_view()),
    path('admin/product-vat-type-list/', AdminVatTypeListAPIView.as_view()),
    path('admin/flash-deal-list/', AdminFlashDealListAPIView.as_view()),
    path('admin/flash-deal-create/', AdminFlashDealCreateAPIView.as_view()),
    path('admin/profile/', AdminProfileAPIView.as_view()),
    path('admin/review-list/', AdminReviewListAPIView.as_view()),
    path('admin/review-inactive/<int:id>/', AdminReviewInactiveAPIView.as_view()),
    path('admin/review-search/', ReviewSearchAPI.as_view()),
    path('admin/attribute-list/', AdminAttributeListAPIView.as_view()),
    path('admin/add-new-attribute/', AdminAddNewAttributeAPIView.as_view()),
    path('admin/update-attribute/<int:id>/', AdminUpdateAttributeAPIView.as_view()),
    path('admin/attribute-values-list/', AdminAttributeValuesListAPIView.as_view()),
    path('admin/add-new-attribute-value/', AdminAddNewAttributeValueAPIView.as_view()),
    path('admin/update-attribute-value/<int:id>/', AdminUpdateAttributeValueAPIView.as_view()),
    path('admin/filter-attribute-list/', AdminFilterAttributeListAPIView.as_view()),
    path('admin/add-new-filter-attribute/', AdminAddNewFilterAttributeAPIView.as_view()),
    path('admin/update-filter-attribute/<int:id>/', AdminUpdateFilterAttributeAPIView.as_view()),
    path('admin/all-order-list/', AdminOrderList.as_view()),
    path('admin/order-view/<int:id>/',AdminOrderViewAPI.as_view()),
    path('admin/order-search/',OrderListSearchAPI.as_view(),),
    path('admin/order-update/<str:id>', AdminOrderUpdateAPI.as_view()),
    path('admin/customer-list/', AdminCustomerListAPIView.as_view()),
    path('admin/support-ticket-list/', AdminTicketListAPIView.as_view()),
    path('admin/support-ticket-details/<int:id>/', AdminTicketDetailsAPIView.as_view()),
    path('admin/support-ticket-status-update/<int:id>/', AdminUpdateTicketStatusAPIView.as_view()),
    path('admin/dashboard-data/', AdminDashboardDataAPIView.as_view()),
]
