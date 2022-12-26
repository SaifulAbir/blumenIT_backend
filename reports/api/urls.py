from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from reports.api.views import SalesReportAPI, SalesReportSearchAPI

urlpatterns = [
    path('reports/sales-report/<int:pagination>/', SalesReportAPI.as_view()),
    path('reports/sales-report/search/<int:pagination>/', SalesReportSearchAPI.as_view()),
]