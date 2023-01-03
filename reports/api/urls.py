from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from reports.api.views import SalesReportAPI, SalesReportSearchAPI, VendorProductReportAPI, VendorProductReportSearchAPI, \
    InHouseProductReportAPI, InHouseProductReportSearchAPI, SellerProductsSaleReportAPI, SellerProductsSaleReportSearchAPI, \
    ProductStockReportAPI, ProductStockReportSearchAPI, ProductWishlistReportAPI, ProductWishlistReportSearchAPI

urlpatterns = [
    path('reports/sales-report/<int:pagination>/', SalesReportAPI.as_view()),
    path('reports/sales-report/search/<int:pagination>/', SalesReportSearchAPI.as_view()),

    path('reports/vendor-product-report/<int:pagination>/', VendorProductReportAPI.as_view()),
    path('reports/vendor-product-report/search/<int:pagination>/', VendorProductReportSearchAPI.as_view()),

    path('reports/in-house-product/<int:pagination>/', InHouseProductReportAPI.as_view()),
    path('reports/in-house-product/search/<int:pagination>/', InHouseProductReportSearchAPI.as_view()),

    path('reports/seller-products-sale/<int:pagination>/', SellerProductsSaleReportAPI.as_view()),
    path('reports/seller-products-sale/search/<int:pagination>/', SellerProductsSaleReportSearchAPI.as_view()),

    path('reports/product-stock/<int:pagination>/', ProductStockReportAPI.as_view()),
    path('reports/product-stock/search/<int:pagination>/', ProductStockReportSearchAPI.as_view()),

    path('reports/product-wishlist/<int:pagination>/', ProductWishlistReportAPI.as_view()),
    path('reports/product-wishlist/search/<int:pagination>/', ProductWishlistReportSearchAPI.as_view()),

]