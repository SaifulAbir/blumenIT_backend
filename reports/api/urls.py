from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from reports.api.views import SalesReportAPI

urlpatterns = [
    path('reports/sales-report/<int:pagination>/', SalesReportAPI.as_view()),

]