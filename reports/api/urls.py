from django.urls import path
from reports.api.views import SalesReportAPI, SalesReportSearchAPI, VendorProductReportAPI, VendorProductReportSearchAPI, \
    InHouseProductReportAPI, InHouseProductReportSearchAPI, SellerProductsSaleReportAPI, SellerProductsSaleReportSearchAPI, ProductStockReportAPI, ProductStockReportSearchAPI, InHouseProductSaleReportAPI, \
    ProductWishlistReportAPI, ProductWishlistReportSearchAPI, InHouseProductSaleReportSearchAPI

urlpatterns = [
    path('admin/reports/sales-report/', SalesReportAPI.as_view()),
    path('admin/reports/sales-report/search/', SalesReportSearchAPI.as_view()),

    path('admin/reports/vendor-product-report/', VendorProductReportAPI.as_view()),
    path('admin/reports/vendor-product-report/search/', VendorProductReportSearchAPI.as_view()),

    path('admin/reports/in-house-product-sale-report/', InHouseProductSaleReportAPI.as_view()),
    path('admin/reports/in-house-product-sale-report/search/', InHouseProductSaleReportSearchAPI.as_view()),

    path('admin/reports/in-house-product/<int:pagination>/', InHouseProductReportAPI.as_view()),
    path('admin/reports/in-house-product/search/', InHouseProductReportSearchAPI.as_view()),

    path('admin/reports/seller-products-sale/', SellerProductsSaleReportAPI.as_view()),
    path('admin/reports/seller-products-sale/search/', SellerProductsSaleReportSearchAPI.as_view()),

    path('admin/reports/product-stock/', ProductStockReportAPI.as_view()),
    path('admin/reports/product-stock/search/', ProductStockReportSearchAPI.as_view()),

    path('admin/reports/product-wishlist/', ProductWishlistReportAPI.as_view()),
    path('admin/reports/product-wishlist/search/', ProductWishlistReportSearchAPI.as_view()),

]