from rest_framework.generics import ListAPIView
from cart.models import Order, OrderItem
from product.models import Product
from vendor.models import Seller
from rest_framework.permissions import IsAuthenticated
from product.pagination import ProductCustomPagination
from reports.serializers import SalesReportSerializer, VendorProductReportSerializer, InHouseProductSerializer, SellerProductSaleSerializer, \
    ProductStockSerializer, ProductWishlistSerializer, InHouseSaleSerializer
from rest_framework.exceptions import ValidationError
from django.db.models import Q

class SalesReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesReportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:

            if self.request.user.is_seller == True:
                queryset = Order.objects.filter(order_item_order__product__seller=Seller.objects.get(seller_user=self.request.user.id)).order_by('-created_at')
            else:
                queryset = Order.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no data in order list."})
        else:
            raise ValidationError(
                {"msg": 'You can not see order report list, because you are not an Admin or a staff or a vendor!'})


class SalesReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesReportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
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
                {"msg": 'You can not search in sale report list, because you are not an Admin or a staff!'})


class VendorProductReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductReportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            # work with dynamic pagination page_size
            # try:
            #     pagination = self.kwargs['pagination']
            # except:
            #     pagination = 10
            # self.pagination_class.page_size = pagination

            queryset = OrderItem.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no product in order items."})
        else:
            raise ValidationError(
                {"msg": 'You can not see vendor product list, because you are not an Admin or a staff!'})


class VendorProductReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductReportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            # work with dynamic pagination page_size
            # try:
            #     pagination = self.kwargs['pagination']
            # except:
            #     pagination = 10
            # self.pagination_class.page_size = pagination


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
                {"msg": 'You can not search in sale report list, because you are not an Admin or a staff!'})


class InHouseProductReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InHouseProductSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Product.objects.filter(in_house_product=True).order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no in-house product available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see in-house product list, because you are not an Admin or a staff!'})


class InHouseProductSaleReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InHouseSaleSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Product.objects.filter(order_item_product__order__in_house_order=True).order_by('-created_at').distinct()
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no in-house order available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see in-house product sale report list, because you are not an Admin or a staff!'})


class InHouseProductSaleReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InHouseProductSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            request = self.request
            search = request.GET.get('search')

            queryset = Product.objects.filter(order_item_product__order__in_house_order=True).order_by('-created_at').distinct()

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in-house product sale report list, because you are not an Admin or a staff!'})


class InHouseProductReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InHouseProductSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            # work with dynamic pagination page_size
            # try:
            #     pagination = self.kwargs['pagination']
            # except:
            #     pagination = 10
            # self.pagination_class.page_size = pagination


            request = self.request
            search = request.GET.get('search')

            queryset = Product.objects.all().order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in sale report list, because you are not an Admin or a staff!'})


class SellerProductsSaleReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerProductSaleSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Seller.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no seller product sale available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see seller product sale list, because you are not an Admin or a staff!'})


class SellerProductsSaleReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerProductSaleSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            # work with dynamic pagination page_size
            # try:
            #     pagination = self.kwargs['pagination']
            # except:
            #     pagination = 10
            # self.pagination_class.page_size = pagination


            request = self.request
            status = request.GET.get('status')

            queryset = Seller.objects.all().order_by('-created_at')

            if status:
                queryset = queryset.filter(Q(status__exact=status))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in seller product sale report list, because you are not an Admin or a staff!'})


class ProductStockReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductStockSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            if self.request.user.is_seller == True:
                queryset = Product.objects.filter(status='PUBLISH',  seller=Seller.objects.get(seller_user=self.request.user.id)).order_by('-created_at')
            else:
                queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no product list available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see product list, because you are not an Admin or a staff!'})


class ProductStockReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductStockSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request
            search = request.GET.get('search')

            if self.request.user.is_seller == True:
                queryset = Product.objects.filter(status='PUBLISH',  seller=Seller.objects.get(seller_user=self.request.user.id)).order_by('-created_at')
            else:
                queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in seller product sale report list, because you are not an Admin or a staff!'})


class ProductWishlistReportAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductWishlistSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            # work with dynamic pagination page_size
            # try:
            #     pagination = self.kwargs['pagination']
            # except:
            #     pagination = 10
            # self.pagination_class.page_size = pagination

            queryset = Product.objects.all().order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no product list available."})
        else:
            raise ValidationError(
                {"msg": 'You can not see product list, because you are not an Admin or a staff!'})


class ProductWishlistReportSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductWishlistSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            request = self.request
            search = request.GET.get('search')

            queryset = Product.objects.all().order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            return queryset

        else:
            raise ValidationError(
                {"msg": 'You can not search in seller product sale report list, because you are not an Admin or a staff!'})