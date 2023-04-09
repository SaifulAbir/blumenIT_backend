from django.urls import path
from vendor.api.views import AdminAddNewSubCategoryAPIView, AdminAddNewSubSubCategoryAPIView, AdminBrandListAPIView, \
    AdminCategoryListAPIView, AdminDeleteCategoryAPIView, AdminDeleteSubCategoryAPIView, \
    AdminShippingClassListAllAPIView, \
    AdminDeleteSubSubCategoryAPIView, AdminProductDeleteAPI, AdminProductViewAPI, AdminSubCategoryListAPIView, \
    AdminSubSubCategoryListAPIView, AdminTagListAPIView, AdminUnitListAPIView, AdminUnitAddAPIView, \
    AdminUnitUpdateAPIView, \
    AdminUnitDeleteAPIView, AdminDiscountListAPIView, AdminShippingCityListAllAPIView, AdminShippingStateListAllAPIView, \
    AdminUpdateCategoryAPIView, AdminUpdateSubCategoryAPIView, AdminUpdateSubSubCategoryAPIView, \
    AdminVatTypeListAPIView, AdminVatTypeAddAPIView, AdminVatTypeUpdateAPIView, AdminVatTypeDeleteAPIView, \
    AdminVideoProviderListAPIView, \
    AdminProductCreateAPIView, AdminSellerCreateAPIView, AdminSellerListAPIView, AdminSellerUpdateAPIView, \
    AdminSellerDeleteAPIView, \
    AdminSellerDetailsAPIView, AdminProductUpdateAPIView, AdminAddNewCategoryAPIView, AdminProductListAPI, \
    AdminFlashDealCreateAPIView, \
    AdminFilterAttributesAPI, AdminProfileAPIView, AdminReviewListAPIView, AdminReviewInactiveAPIView, ReviewSearchAPI, \
    AdminAttributeListAPIView, AdminAddNewAttributeAPIView, AdminUpdateAttributeAPIView, \
    AdminAddNewAttributeValueAPIView, AdminUpdateAttributeValueAPIView, AdminFilterAttributeListAPIView, \
    AdminAddNewFilterAttributeAPIView, \
    AdminProductListSearchAPI, AdminOrderList, AdminOrderViewAPI, OrderListSearchAPI, AdminOrderUpdateAPI, \
    AdminUpdateFilterAttributeAPIView, AdminCustomerListAPIView, AdminTicketListAPIView, AdminTicketDetailsAPIView, \
    AdminTicketStatusUpdateAPIView, AdminDashboardDataAPIView, AdminBrandCreateAPIView, AdminBrandDeleteAPIView, \
    AdminFlashDealListAPIView, AdminWarrantyListAPIView, AdminShippingClassListAPIView, \
    AdminSpecificationTitleListAPIView, AdminFlashDealUpdateAPIView, AdminFlashDealDeleteAPIView, \
    AdminSubscribersListAPIView, \
    AdminSubscriberDeleteAPIView, AdminCorporateDealListAPIView, AdminCorporateDealDeleteAPIView, \
    AdminAttributeDeleteAPIView, \
    AdminOrderDeleteAPIView, AdminCouponCreateAPIView, AdminCouponListAPIView, AdminCouponUpdateAPIView, \
    AdminCouponDeleteAPIView, \
    AdminCustomerDeleteAPIView, AdminBrandUpdateAPIView, AdminOffersListAPIView, AdminOffersCreateAPIView, \
    AdminOffersDetailsAPIView, AdminDeleteWebsiteConfigurationImageAPIView, \
    AdminOffersUpdateAPIView, AdminOffersDeleteAPIView, AdminPosProductListAPI, AdminShippingCountryListAPIView, \
    AdminShippingCountryListFilterAPIView, AdminShippingCountryAddAPIView, AdminShippingCountryUpdateAPIView, \
    AdminShippingCountryDeleteAPIView, AdminShippingCityListAPIView, AdminShippingCityAddAPIView, \
    AdminShippingCityUpdateAPIView, AdminSellerOrderList, \
    AdminShippingCityDeleteAPIView, AdminShippingStateListAPIView, AdminShippingStateAddAPIView, \
    AdminShippingStateUpdateAPIView, AdminSubscribersListAllAPIView, AdminCustomerListAllAPIView, \
    AdminPosSearchAPI, AdminPosOrderAPIView, AdminShippingStateDeleteAPIView, AdminShippingClassAddAPIView, \
    AdminShippingClassUpdateAPIView, AdminShippingClassDeleteAPIView, AdminAttributeListAllAPIView, \
    AdminWebsiteConfigurationCreateAPIView, AdminUpdateSubSubCategoryDetailsAPIView, \
    AdminCategoryAllListAPIView, AdminSubCategoryListAllAPIView, AdminSubSubCategoryAllListAPIView, \
    AdminBrandListAllAPIView, AdminSubCategoryToggleUpdateAPIView, AdminUpdateSubCategoryDetailsAPIView, \
    AdminUnitListAllAPIView, AdminSellerListAllAPIView, AdminVatTypeListAllAPIView, AdminVideoProviderListAllAPIView, \
    AdminDiscountTypeListAllAPIView, AdminFilterAttributeListAllAPIView, AdminFlashDealListAllAPIView, \
    AdminWarrantyListAllAPIView, AdminWebsiteConfigurationUpdateAPIView, AdminUpdateCategoryDetailsAPIView, \
    AdminVideoProviderCreateAPIView, AdminVideoProviderUpdateAPIView, AdminSpecificationTitleListAllAPIView, \
    AdminVideoProviderDeleteAPI, AdminTicketDeleteAPIView, AdminTicketReplyCreateAPIView, \
    AdminProductToggleUpdateAPIView, AdminCategoryToggleUpdateAPIView, AdminBlogToggleUpdateAPIView, \
    AdminProductReviewToggleAPIView, AdminAdvertisementListAPIView, AdminProductUpdateDetailsAPIView, \
    AdminShippingCountryListAllAPIView, AdminRequestQuoteDetailsAPIView, AdminRequestQuoteDeleteAPIView, \
    AdminAdvertisementCreateAPIView, AdminAdvertisementUpdateAPIView, AdminAdvertisementDeleteAPIView, \
    AdminContactUsListAPIView, AdminFilterAttributeValueListAllAPIView, AdminSpecificationDeleteAPIView, \
    AdminPosCustomerProfileAPIView, AdminCorporateDealDetailsAPIView, AdminRequestQuoteListAPIView, \
    AdminContactUsDetailsAPIView, AdminOffersListAllAPIView, AdminSpecificationCreateAPIView, \
    AdminContactUsDeleteAPIView, AdminPosCustomerCreateAPIView, AdminWebsiteConfigurationViewAPIView, \
    AdminOfferCategoryListAPIView, AdminBrandIsGamingToggleAPIView, AdminCategoryIsPcBuilderToggleAPIView, \
    SellerListAPIView, AdminWebsiteGeneralSettingsView, AdminWebsiteGeneralSettingsUpdateAPIView, \
    AdminDeleteAttributeValueAPIView

urlpatterns = [

    # seller apies
    path('admin/seller-create/', AdminSellerCreateAPIView.as_view()),
    path('seller-list/', SellerListAPIView.as_view()),
    path('admin/seller-list/', AdminSellerListAPIView.as_view()),
    path('admin/seller-update/<int:id>/', AdminSellerUpdateAPIView.as_view()),
    path('admin/seller-delete/<int:id>/', AdminSellerDeleteAPIView.as_view()),
    path('admin/seller-details/<int:id>/', AdminSellerDetailsAPIView.as_view()),
    path('admin/product-create/', AdminProductCreateAPIView.as_view()),
    path('admin/product-update/<str:slug>/',AdminProductUpdateAPIView.as_view()),
    path('admin/product-update-details/<str:slug>/',AdminProductUpdateDetailsAPIView.as_view()),
    path('admin/product-list/', AdminProductListAPI.as_view()),
    path('admin/product-list-search/', AdminProductListSearchAPI.as_view()),
    path('admin/product-delete/<str:slug>/',AdminProductDeleteAPI.as_view()),
    path('admin/product-view/<str:slugi>/',AdminProductViewAPI.as_view()),
    path('admin/category-list/', AdminCategoryListAPIView.as_view()),
    path('admin/add-new-category/', AdminAddNewCategoryAPIView.as_view()),
    path('admin/update-category-details/<int:id>/', AdminUpdateCategoryDetailsAPIView.as_view()),
    path('admin/update-category/<int:pk>/', AdminUpdateCategoryAPIView.as_view()),
    path('admin/delete-category/<int:id>/', AdminDeleteCategoryAPIView.as_view()),
    path('admin/sub-category-list/<int:cid>/',AdminSubCategoryListAPIView.as_view()),
    path('admin/add-new-sub-category/', AdminAddNewSubCategoryAPIView.as_view()),
    path('admin/update-sub-category-details/<int:id>/', AdminUpdateSubCategoryDetailsAPIView.as_view()),
    path('admin/update-sub-category/<int:pk>/', AdminUpdateSubCategoryAPIView.as_view()),
    path('admin/delete-sub-category/<int:id>/', AdminDeleteSubCategoryAPIView.as_view()),
    path('admin/sub-sub-category-list/<int:sid>/',AdminSubSubCategoryListAPIView.as_view()),
    path('admin/add-new-sub-sub-category/', AdminAddNewSubSubCategoryAPIView.as_view()),
    path('admin/update-sub-sub-category-details/<int:id>/', AdminUpdateSubSubCategoryDetailsAPIView.as_view()),
    path('admin/update-sub-sub-category/<int:pk>/', AdminUpdateSubSubCategoryAPIView.as_view()),
    path('admin/delete-sub-sub-category/<int:id>/', AdminDeleteSubSubCategoryAPIView.as_view()),


    # product create supportive list apies
    path('admin/category-list-all/', AdminCategoryAllListAPIView.as_view()),
    path('admin/sub-category-list-all/<int:cid>/', AdminSubCategoryListAllAPIView.as_view()),
    path('admin/sub-sub-category-list-all/<int:sid>/', AdminSubSubCategoryAllListAPIView.as_view()),
    path('admin/brand-list-all/', AdminBrandListAllAPIView.as_view()),
    path('admin/unit-list-all/', AdminUnitListAllAPIView.as_view()),
    path('admin/seller-list-all/', AdminSellerListAllAPIView.as_view()),
    path('admin/vat-type-list-all/', AdminVatTypeListAllAPIView.as_view()),
    path('admin/video-provider-list-all/', AdminVideoProviderListAllAPIView.as_view()),
    path('admin/discount-type-list-all/', AdminDiscountTypeListAllAPIView.as_view()),
    path('admin/filter-attribute-list-all/', AdminFilterAttributeListAllAPIView.as_view()),
    path('admin/filter-attribute-value-list-all/<int:atid>/', AdminFilterAttributeValueListAllAPIView.as_view()),
    path('admin/flash-deal-list-all/', AdminFlashDealListAllAPIView.as_view()),
    path('admin/offers-list-all/', AdminOffersListAllAPIView.as_view()),
    path('admin/warranty-list-all/', AdminWarrantyListAllAPIView.as_view()),
    path('admin/specification-title-list-all/', AdminSpecificationTitleListAllAPIView.as_view()),
    path('admin/attribute-list-all/', AdminAttributeListAllAPIView.as_view()),


    # Tag related apies
    path('admin/admin-tag-list/', AdminTagListAPIView.as_view()),


    # Discount related apies
    path('admin/admin-discount-list/', AdminDiscountListAPIView.as_view()),


    # Review related apies
    path('admin/review-list/', AdminReviewListAPIView.as_view()),
    path('admin/review-inactive/<int:id>/', AdminReviewInactiveAPIView.as_view()),
    path('admin/review-search/', ReviewSearchAPI.as_view()),


    # Video provider related apies
    path('admin/admin-video-provider-list/', AdminVideoProviderListAPIView.as_view()),
    path('admin/admin-video-provider-create/', AdminVideoProviderCreateAPIView.as_view()),
    path('admin/admin-video-provider-update/<int:id>/', AdminVideoProviderUpdateAPIView.as_view()),
    path('admin/admin-video-provider-delete/<int:id>/', AdminVideoProviderDeleteAPI.as_view()),


    # order apies
    path('admin/all-order-list/', AdminOrderList.as_view()),
    path('admin/seller-order/', AdminSellerOrderList.as_view()),
    path('admin/order-view/<int:id>/', AdminOrderViewAPI.as_view()),
    path('admin/order-update/<int:id>/', AdminOrderUpdateAPI.as_view()),
    path('admin/order-list-search/', OrderListSearchAPI.as_view()),
    path('admin/order-delete/<int:id>/', AdminOrderDeleteAPIView.as_view()),


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
    path('admin/delete-attribute-value/<int:id>/', AdminDeleteAttributeValueAPIView.as_view()),
    path('admin/filter-attribute-list/', AdminFilterAttributeListAPIView.as_view()),
    path('admin/add-new-filter-attribute/', AdminAddNewFilterAttributeAPIView.as_view()),
    path('admin/update-filter-attribute/<int:id>/', AdminUpdateFilterAttributeAPIView.as_view()),
    path('admin/filtering-attributes/<int:id>/<str:type>/', AdminFilterAttributesAPI.as_view()),


    # corporate apies
    path('admin/corporate-deal-list/', AdminCorporateDealListAPIView.as_view()),
    path('admin/corporate-deal-details/<int:id>/', AdminCorporateDealDetailsAPIView.as_view()),
    path('admin/corporate-deal-delete/<int:id>/', AdminCorporateDealDeleteAPIView.as_view()),


    # Request quote apies
    path('admin/request-quote-list/', AdminRequestQuoteListAPIView.as_view()),
    path('admin/request-quote-details/<int:id>/', AdminRequestQuoteDetailsAPIView.as_view()),
    path('admin/request-quote-delete/<int:id>/', AdminRequestQuoteDeleteAPIView.as_view()),


    # Contact Us apies
    path('admin/contact-us-list/', AdminContactUsListAPIView.as_view()),
    path('admin/contact-us-details/<int:id>/', AdminContactUsDetailsAPIView.as_view()),
    path('admin/contact-us-delete/<int:id>/', AdminContactUsDeleteAPIView.as_view()),


    # subscribers apies
    path('admin/subscribers-list-all/', AdminSubscribersListAllAPIView.as_view()),
    path('admin/subscribers-list/', AdminSubscribersListAPIView.as_view()),
    path('admin/subscriber-delete/<int:id>/', AdminSubscriberDeleteAPIView.as_view()),


    # customer apies
    path('admin/customer-list-all/', AdminCustomerListAllAPIView.as_view()),
    path('admin/customer-list/', AdminCustomerListAPIView.as_view()),
    path('admin/customer-delete/<int:id>/', AdminCustomerDeleteAPIView.as_view()),


    # shipping class apies
    path('admin/shipping-country-add/', AdminShippingCountryAddAPIView.as_view()),
    path('admin/shipping-country-list/', AdminShippingCountryListAPIView.as_view()),
    path('admin/shipping-country-list-all/', AdminShippingCountryListAllAPIView.as_view()),
    path('admin/shipping-country-filter/', AdminShippingCountryListFilterAPIView.as_view()),
    path('admin/shipping-country-update/<int:id>/', AdminShippingCountryUpdateAPIView.as_view()),
    path('admin/shipping-country-delete/<int:id>/', AdminShippingCountryDeleteAPIView.as_view()),
    path('admin/shipping-city-list/', AdminShippingCityListAPIView.as_view()),
    path('admin/shipping-city-list-all/', AdminShippingCityListAllAPIView.as_view()),
    path('admin/shipping-city-add/', AdminShippingCityAddAPIView.as_view()),
    path('admin/shipping-city-update/<int:id>/', AdminShippingCityUpdateAPIView.as_view()),
    path('admin/shipping-city-delete/<int:id>/', AdminShippingCityDeleteAPIView.as_view()),
    path('admin/shipping-state-list/', AdminShippingStateListAPIView.as_view()),
    path('admin/shipping-state-list-all/', AdminShippingStateListAllAPIView.as_view()),
    path('admin/shipping-state-add/', AdminShippingStateAddAPIView.as_view()),
    path('admin/shipping-state-update/<int:id>/', AdminShippingStateUpdateAPIView.as_view()),
    path('admin/shipping-state-delete/<int:id>/', AdminShippingStateDeleteAPIView.as_view()),
    path('admin/shipping-class-list/', AdminShippingClassListAPIView.as_view()),
    path('admin/shipping-class-list-all/', AdminShippingClassListAllAPIView.as_view()),
    path('admin/shipping-class-add/', AdminShippingClassAddAPIView.as_view()),
    path('admin/shipping-class-update/<int:id>/', AdminShippingClassUpdateAPIView.as_view()),
    path('admin/shipping-class-delete/<int:id>/', AdminShippingClassDeleteAPIView.as_view()),


    # warranty apies
    path('admin/warranty-list/', AdminWarrantyListAPIView.as_view()),


    # specification apies
    path('admin/specification-title-list/', AdminSpecificationTitleListAPIView.as_view()),
    path('admin/specification-create/', AdminSpecificationCreateAPIView.as_view()),
    path('admin/specification-delete/<int:id>/', AdminSpecificationDeleteAPIView.as_view()),


    # coupon apies
    path('admin/coupon-create/', AdminCouponCreateAPIView.as_view()),
    path('admin/coupon-list/', AdminCouponListAPIView.as_view()),
    path('admin/coupon-update/<int:id>/', AdminCouponUpdateAPIView.as_view()),
    path('admin/coupon-delete/<int:id>/', AdminCouponDeleteAPIView.as_view()),


    # offers apies
    path('admin/offers-category-list/', AdminOfferCategoryListAPIView.as_view()),
    path('admin/offers-list/', AdminOffersListAPIView.as_view()),
    path('admin/offers-details/<int:id>/', AdminOffersDetailsAPIView.as_view()),
    path('admin/offers-create/', AdminOffersCreateAPIView.as_view()),
    path('admin/offers-update/<int:id>/', AdminOffersUpdateAPIView.as_view()),
    path('admin/offers-delete/<int:id>/', AdminOffersDeleteAPIView.as_view()),


    # units apies
    path('admin/product-unit-list/', AdminUnitListAPIView.as_view()),
    path('admin/product-unit-add/', AdminUnitAddAPIView.as_view()),
    path('admin/product-unit-update/<int:id>/', AdminUnitUpdateAPIView.as_view()),
    path('admin/product-unit-delete/<int:id>/', AdminUnitDeleteAPIView.as_view()),


    # vat apies
    path('admin/product-vat-type-list/', AdminVatTypeListAPIView.as_view()),
    path('admin/product-vat-type-add/', AdminVatTypeAddAPIView.as_view()),
    path('admin/product-vat-type-update/<int:id>/', AdminVatTypeUpdateAPIView.as_view()),
    path('admin/product-vat-type-delete/<int:id>/', AdminVatTypeDeleteAPIView.as_view()),


    # others
    path('admin/profile/', AdminProfileAPIView.as_view()),
    path('admin/dashboard-data/', AdminDashboardDataAPIView.as_view()),


    # pos apies
    path('admin/pos-product-list/', AdminPosProductListAPI.as_view()),
    path('admin/pos-product-search-list/', AdminPosSearchAPI.as_view()),
    path('admin/pos-order/', AdminPosOrderAPIView.as_view()),
    path('admin/pos-customer-list/', AdminPosCustomerProfileAPIView.as_view()),
    path('admin/pos-customer-create/', AdminPosCustomerCreateAPIView.as_view()),



    # ticket apies
    path('admin/ticket-list/', AdminTicketListAPIView.as_view()),
    path('admin/ticket-details/<int:id>/', AdminTicketDetailsAPIView.as_view()),
    path('admin/ticket-status-update/<int:id>/', AdminTicketStatusUpdateAPIView.as_view()),
    path('admin/ticket-delete/<int:id>/', AdminTicketDeleteAPIView.as_view()),
    path('admin/ticket-reply-create/', AdminTicketReplyCreateAPIView.as_view()),


    #toggle apies
    path('admin/toggle-category/<int:pk>/', AdminCategoryToggleUpdateAPIView.as_view()),
    path('admin/toggle-sub-category/<int:pk>/', AdminSubCategoryToggleUpdateAPIView.as_view()),
    path('admin/toggle-product/<int:pk>/', AdminProductToggleUpdateAPIView.as_view()),
    path('admin/toggle-blog/<int:pk>/', AdminBlogToggleUpdateAPIView.as_view()),
    path('admin/toggle-product-review/<int:pk>/', AdminProductReviewToggleAPIView.as_view()),
    path('admin/toggle-brand-is-gaming/<int:pk>/', AdminBrandIsGamingToggleAPIView.as_view()),
    path('admin/toggle-category-is-pc-builder/<int:pk>/', AdminCategoryIsPcBuilderToggleAPIView.as_view()),
    # path('admin/toggle-sub-category-pcbuilder/<int:pk>/', AdminSubCategoryToggleUpdateAPIView.as_view()),



    # advertisement apies
    path('admin/advertisement-poster-list/', AdminAdvertisementListAPIView.as_view()),
    path('admin/advertisement-poster-create/', AdminAdvertisementCreateAPIView.as_view()),
    path('admin/advertisement-poster-update/<int:id>/', AdminAdvertisementUpdateAPIView.as_view()),
    path('admin/advertisement-poster-delete/<int:id>/', AdminAdvertisementDeleteAPIView.as_view()),


    # website-configuration apies
    path('admin/website-configuration/', AdminWebsiteConfigurationCreateAPIView.as_view()),
    path('admin/website-configuration-view/', AdminWebsiteConfigurationViewAPIView.as_view()),
    path('admin/website-configuration-update/<int:pk>/', AdminWebsiteConfigurationUpdateAPIView.as_view()),

    path('admin/delete-website-configuration-image/<int:id>/', AdminDeleteWebsiteConfigurationImageAPIView.as_view()),

    # general-settings api
    path('admin/website-general-settings-view/', AdminWebsiteGeneralSettingsView.as_view()),
    path('admin/website-general-settings-update/<int:pk>/', AdminWebsiteGeneralSettingsUpdateAPIView.as_view()),
]

