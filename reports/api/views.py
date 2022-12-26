from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from cart.models import Order
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.pagination import ProductCustomPagination
from reports.serializers import SalesReportSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import Q

class SalesReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesReportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            # work with dynamic pagination page_size
            try:
                pagination = self.kwargs['pagination']
            except:
                pagination = 10
            self.pagination_class.page_size = pagination

            queryset = Order.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no ticket in your ticket list."})
        else:
            raise ValidationError(
                {"msg": 'You can not see sale report list, because you are not an Admin!'})


class SalesReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesReportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            # work with dynamic pagination page_size
            try:
                pagination = self.kwargs['pagination']
            except:
                pagination = 10
            self.pagination_class.page_size = pagination


            request = self.request
            query = request.GET.get('delivery_status')

            queryset = Order.objects.all().order_by('-created_at')

            if query:
                queryset = queryset.filter(Q(order_id__icontains=query))


            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in sale report list, because you are not an Admin!'})
