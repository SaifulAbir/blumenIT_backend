from rest_framework.generics import ListAPIView
from cart.models import Order, OrderItem
from product.models import Product
from vendor.models import Seller
from rest_framework.permissions import IsAuthenticated
from product.pagination import ProductCustomPagination
from reports.serializers import SalesReportSerializer, VendorProductReportSerializer, InHouseProductSerializer, SellerProductSaleSerializer, \
    ProductStockSerializer, ProductWishlistSerializer
from rest_framework.exceptions import ValidationError
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
            seller_id = request.GET.get('seller_id')

            queryset = OrderItem.objects.all().order_by('-created_at')

            if order_status:
                queryset = queryset.filter(Q(order__order_status__icontains=order_status))

            # date
            if start_date:
                queryset = queryset.filter(Q(order__order_date__range=(start_date,end_date)) | Q(order__order_date__icontains=start_date))

            if seller_id:
                queryset = queryset.filter(Q(order__vendor__exact=seller_id))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in sale report list, because you are not an Admin!'})


class InHouseProductReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InHouseProductSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            # work with dynamic pagination page_size
            try:
                pagination = self.kwargs['pagination']
            except:
                pagination = 10
            self.pagination_class.page_size = pagination

            queryset = Product.objects.filter(in_house_product=True).order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no in-house product available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see in-house product list, because you are not an Admin!'})


class InHouseProductReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InHouseProductSerializer
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
            category_id = request.GET.get('category_id')

            queryset = Product.objects.all().order_by('-created_at')

            if category_id:
                queryset = queryset.filter(Q(category__exact=category_id))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in sale report list, because you are not an Admin!'})


class SellerProductsSaleReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerProductSaleSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            # work with dynamic pagination page_size
            try:
                pagination = self.kwargs['pagination']
            except:
                pagination = 10
            self.pagination_class.page_size = pagination

            queryset = Seller.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no seller product sale available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see seller product sale list, because you are not an Admin!'})


class SellerProductsSaleReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerProductSaleSerializer
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
            status = request.GET.get('status')

            queryset = Seller.objects.all().order_by('-created_at')

            if status:
                queryset = queryset.filter(Q(status__exact=status))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in seller product sale report list, because you are not an Admin!'})


class ProductStockReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductStockSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            # work with dynamic pagination page_size
            try:
                pagination = self.kwargs['pagination']
            except:
                pagination = 10
            self.pagination_class.page_size = pagination

            queryset = Product.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no product list available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see product list, because you are not an Admin!'})


class ProductStockReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductStockSerializer
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
            category_id = request.GET.get('category_id')

            queryset = Product.objects.all().order_by('-created_at')

            if category_id:
                queryset = queryset.filter(Q(category=category_id))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in seller product sale report list, because you are not an Admin!'})


class ProductWishlistReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductWishlistSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            # work with dynamic pagination page_size
            try:
                pagination = self.kwargs['pagination']
            except:
                pagination = 10
            self.pagination_class.page_size = pagination

            queryset = Product.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no product list available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see product list, because you are not an Admin!'})


class ProductWishlistReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductWishlistSerializer
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
            category_id = request.GET.get('category_id')

            queryset = Product.objects.all().order_by('-created_at')

            if category_id:
                queryset = queryset.filter(Q(category=category_id))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in seller product sale report list, because you are not an Admin!'})