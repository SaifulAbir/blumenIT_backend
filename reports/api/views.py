from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from cart.models import Order, OrderItem
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.pagination import ProductCustomPagination
from reports.serializers import SalesReportSerializer, VendorProductReportSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import Q
import datetime

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
                raise ValidationError({"msg": "There is no data in order list."})
        else:
            raise ValidationError(
                {"msg": 'You can not see order report list, because you are not an Admin!'})


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
            order_status = request.GET.get('order_status')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            order_code = request.GET.get('order_code')
            phone = request.GET.get('phone')

            queryset = Order.objects.all().order_by('-created_at')

            if order_status:
                queryset = queryset.filter(Q(order_status__icontains=order_status))

            # date
            if start_date:
                # print(start_date)
                # try:
                #     check_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                # print(dt)
                queryset = queryset.filter(Q(order_date__range=(start_date,end_date)) | Q(order_date__icontains=start_date))

            if order_code:
                queryset = queryset.filter(Q(order_id__icontains=order_code))

            if phone:
                queryset = queryset.filter(Q(user__phone__icontains=phone))


            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in sale report list, because you are not an Admin!'})


class VendorProductReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductReportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            # work with dynamic pagination page_size
            try:
                pagination = self.kwargs['pagination']
            except:
                pagination = 10
            self.pagination_class.page_size = pagination

            queryset = OrderItem.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no product in order items."})
        else:
            raise ValidationError(
                {"msg": 'You can not see vendor product list, because you are not an Admin!'})


class VendorProductReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductReportSerializer
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
            order_status = request.GET.get('order_status')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            seller = request.GET.get('seller')

            queryset = OrderItem.objects.all().order_by('-created_at')

            if order_status:
                queryset = queryset.filter(Q(order__order_status__icontains=order_status))

            # date
            if start_date:
                queryset = queryset.filter(Q(order__order_date__range=(start_date,end_date)) | Q(order__order_date__icontains=start_date))

            if seller:
                queryset = queryset.filter(Q(order_id__icontains=seller))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in sale report list, because you are not an Admin!'})

