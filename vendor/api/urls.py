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
    AdminAttributeListAPIView, AdminAddNewAttributeAPIView, AdminUpdateAttributeAPIView, \
    AdminAddNewAttributeValueAPIView, AdminUpdateAttributeValueAPIView, AdminFilterAttributeListAPIView, AdminAddNewFilterAttributeAPIView, \
    AdminProductListSearchAPI, AdminOrderList, AdminOrderViewAPI, OrderListSearchAPI, AdminOrderUpdateAPI, \
    AdminUpdateFilterAttributeAPIView, AdminCustomerListAPIView, AdminTicketListAPIView, AdminTicketDetailsAPIView, \
    AdminUpdateTicketStatusAPIView, AdminDashboardDataAPIView, AdminBrandCreateAPIView, AdminBrandDeleteAPIView, \
    AdminFlashDealListAPIView, AdminWarrantyListAPIView, AdminShippingClassListAPIView, \
    AdminSpecificationTitleListAPIView, AdminFlashDealUpdateAPIView, AdminFlashDealDeleteAPIView, AdminSubscribersListAPIView, \
    AdminSubscriberDeleteAPIView, AdminCorporateDealListAPIView, AdminCorporateDealDeleteAPIView, AdminAttributeDeleteAPIView, \
    AdminOrderDeleteAPIView, AdminCouponCreateAPIView, AdminCouponListAPIView, AdminCouponUpdateAPIView, AdminCouponDeleteAPIView, \
    AdminCustomerDeleteAPIView, AdminBrandUpdateAPIView, AdminOffersListAPIView, AdminOffersCreateAPIView, AdminOffersDetailsAPIView, \
    AdminOffersUpdateAPIView, AdminOffersDeleteAPIView, AdminPosProductListAPI, AdminPosSearchAPI


urlpatterns = [

    # seller apies
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


    # flash deal apies
    path('admin/flash-deal-list/', AdminFlashDealListAPIView.as_view()),
    path('admin/flash-deal-create/', AdminFlashDealCreateAPIView.as_view()),
    path('admin/flash-deal-update/<int:id>/', AdminFlashDealUpdateAPIView.as_view()),
    path('admin/flash-deal-delete/<int:id>/', AdminFlashDealDeleteAPIView.as_view()),


    # brand apies
    path('admin/product-brand-list/', AdminBrandListAPIView.as_view()),
    path('admin/brand-create/', AdminBrandCreateAPIView.as_view()),
    path('admin/brand-update/<int:id>/', AdminBrandUpdateAPIView.as_view()),
    path('admin/brand-delete/<int:id>/', AdminBrandDeleteAPIView.as_view()),


    # attribute apies
    path('admin/add-new-attribute/', AdminAddNewAttributeAPIView.as_view()),
    path('admin/attribute-list/', AdminAttributeListAPIView.as_view()),
    path('admin/attribute-delete/<int:id>/', AdminAttributeDeleteAPIView.as_view()),
    path('admin/update-attribute/<int:id>/', AdminUpdateAttributeAPIView.as_view()),
    path('admin/add-new-attribute-value/', AdminAddNewAttributeValueAPIView.as_view()),
    path('admin/update-attribute-value/<int:id>/', AdminUpdateAttributeValueAPIView.as_view()),
    path('admin/filter-attribute-list/', AdminFilterAttributeListAPIView.as_view()),
    path('admin/add-new-filter-attribute/', AdminAddNewFilterAttributeAPIView.as_view()),
    path('admin/update-filter-attribute/<int:id>/', AdminUpdateFilterAttributeAPIView.as_view()),
    path('admin/filtering-attributes/<int:id>/<str:type>/', AdminFilterAttributesAPI.as_view()),


    # corporate apies
    path('admin/corporate-deal-list/', AdminCorporateDealListAPIView.as_view()),
    path('admin/corporate-deal-delete/<int:id>/', AdminCorporateDealDeleteAPIView.as_view()),


    # subscribers apies
    path('admin/subscribers-list/', AdminSubscribersListAPIView.as_view()),
    path('admin/subscriber-delete/<int:id>/', AdminSubscriberDeleteAPIView.as_view()),


    # customer apies
    path('admin/customer-list/', AdminCustomerListAPIView.as_view()),
    path('admin/customer-delete/<int:id>/', AdminCustomerDeleteAPIView.as_view()),


    # shipping class apies
    path('admin/shipping-class-list/', AdminShippingClassListAPIView.as_view()),


    # warranty apies
    path('admin/warranty-list/', AdminWarrantyListAPIView.as_view()),


    # specification apies
    path('admin/specification-title-list/', AdminSpecificationTitleListAPIView.as_view()),


    # coupon apies
    path('admin/coupon-create/', AdminCouponCreateAPIView.as_view()),
    path('admin/coupon-list/', AdminCouponListAPIView.as_view()),
    path('admin/coupon-update/<int:id>/', AdminCouponUpdateAPIView.as_view()),
    path('admin/coupon-delete/<int:id>/', AdminCouponDeleteAPIView.as_view()),


    # offers apies
    path('admin/offers-list/', AdminOffersListAPIView.as_view()),
    path('admin/offers-details/<int:id>/', AdminOffersDetailsAPIView.as_view()),
    path('admin/offers-create/', AdminOffersCreateAPIView.as_view()),
    path('admin/offers-update/<int:id>/', AdminOffersUpdateAPIView.as_view()),
    path('admin/offers-delete/<int:id>/', AdminOffersDeleteAPIView.as_view()),


    # others
    path('admin/profile/', AdminProfileAPIView.as_view()),
    path('admin/dashboard-data/', AdminDashboardDataAPIView.as_view()),

    path('admin/subscribers-list/', AdminSubscribersListAPIView.as_view()),
    path('admin/subscriber-delete/<int:id>/', AdminSubscriberDeleteAPIView.as_view()),
    path('admin/corporate-deal-list/', AdminCorporateDealListAPIView.as_view()),
    path('admin/corporate-deal-delete/<int:id>/', AdminCorporateDealDeleteAPIView.as_view()),
    path('admin/pos-product-list/', AdminPosProductListAPI.as_view()),
    path('admin/pos-product-search/', AdminPosSearchAPI.as_view()),
]

