from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from reports.api.views import SalesReportAPI, SalesReportSearchAPI, VendorProductReportAPI, VendorProductReportSearchAPI, \
    InHouseProductReportAPI, InHouseProductReportSearchAPI, SellerProductsSaleReportAPI

urlpatterns = [
    path('reports/sales-report/<int:pagination>/', SalesReportAPI.as_view()),
    path('reports/sales-report/search/<int:pagination>/', SalesReportSearchAPI.as_view()),

    path('reports/vendor-product-report/<int:pagination>/', VendorProductReportAPI.as_view()),
    path('reports/vendor-product-report/search/<int:pagination>/', VendorProductReportSearchAPI.as_view()),

    path('reports/in-house-product/<int:pagination>/', InHouseProductReportAPI.as_view()),
    path('reports/in-house-product/search/<int:pagination>/', InHouseProductReportSearchAPI.as_view()),

    path('reports/seller-products-sale/<int:pagination>/', SellerProductsSaleReportAPI.as_view()),

]