
from django.utils import timezone
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, DestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from product.serializers import DiscountTypeSerializer
from cart.serializers import CheckoutDetailsSerializer, CheckoutSerializer, \
    OrderItemSerializer, OrderSerializer, PaymentTypesListSerializer, WishlistSerializer, \
    ApplyCouponSerializer, CouponSerializer, DeliveryAddressSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Product, DiscountTypes
from cart.models import BillingAddress, Order, OrderItem, PaymentType, Coupon, UseRecordOfCoupon, Wishlist, VendorOrder, \
    DeliveryAddress
from user.models import User


class CouponCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CouponSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(CouponCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create coupon, because you are not an Admin!'})


class CouponListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CouponSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Coupon.objects.all()
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Vat types does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view coupon list, because you are not an Admin!'})


class CouponUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(CouponUpdateAPIView, self).put(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not update coupon, because you are not an Admin!'})


class DiscountTypeCreateAPIView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = DiscountTypeSerializer

    def post(self, request):
        discount_type = DiscountTypeSerializer(data=request.data)

        if DiscountTypes.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')

        if discount_type.is_valid():
            discount_type.save()
            return Response(discount_type.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DiscountTypeListAPI(ListAPIView):

    permission_classes = [AllowAny]
    queryset = DiscountTypes.objects.all()
    serializer_class = DiscountTypeSerializer


class CheckoutAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSerializer

    def post(self, request, *args, **kwargs):
        return super(CheckoutAPIView, self).post(request, *args, **kwargs)


class ApplyCouponAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ApplyCouponSerializer

    def get(self, request, code, uid):
        try:
            code = self.kwargs['code']
            uid = self.kwargs['uid']

            code_exist = Coupon.objects.filter(code=code, is_active=True).exists()
            if code_exist:
                coupon_obj = Coupon.objects.filter(code=code)
                start_date_time = coupon_obj[0].start_time
                end_date_time = coupon_obj[0].end_time

                current_time = timezone.now()

                if current_time > start_date_time and current_time < end_date_time:
                    number_of_uses = int(coupon_obj[0].number_of_uses)
                    if number_of_uses > 0:
                        user = User.objects.filter(id=uid).exists()
                        if user:
                            user_obj = User.objects.filter(id=uid)
                            check_in_use_coupon_record = UseRecordOfCoupon.objects.filter(
                                coupon_id=coupon_obj[0].id, user_id=user_obj[0].id).exists()
                            if check_in_use_coupon_record:
                                return Response({"status": "You already used this coupon!"})
                            else:
                                return Response({"status": "Authentic coupon.", "amount": coupon_obj[0].amount, "coupon_id": coupon_obj[0].id})
                        else:
                            return Response({"status": "User doesn't exist!"})
                    else:
                        return Response({"status": "Invalid coupon!"})
                else:
                    if current_time > end_date_time:
                        coupon_obj.update(is_active=False)
                    return Response({"status": "Invalid coupon!"})
            else:
                return Response({"status": "Invalid coupon!"})
        except:
            return Response({"status": "Something went wrong, contact with developer!"})


class PaymentMethodsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PaymentTypesListSerializer

    def get_queryset(self):
        queryset = PaymentType.objects.filter(status=True)
        return queryset




# class CheckoutDetailsAPIView(RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CheckoutDetailsSerializer
#     lookup_field = 'oid'
#     lookup_url_kwarg = 'oid'

#     def get_object(self):
#         oid = self.kwargs['oid']
#         try:
#             query = Order.objects.get(id=int(oid), user=self.request.user)
#             return query
#         except:
#             raise ValidationError(
#                 {"details": "Order doesn't exist, or this is not your order."})


# class CartList(ListAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = CartListSerializer
#     lookup_field = 'uid'
#     lookup_url_kwarg = "uid"
#     def get_queryset(self):
#         uid = self.kwargs['uid']
#         user = User.objects.get(id = uid)
#         query = OrderItem.objects.filter(user=user,ordered=False)
#         return query


# class PaymentTypeCreateAPIView(CreateAPIView):
#     serializer_class = PaymentTypeCreateSerializer

#     def post(self, request, *args, **kwargs):
#         return super(PaymentTypeCreateAPIView, self).post(request, *args, **kwargs)

# class ActiveCouponlistView(ListAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = ActiveCouponListSerializer
#     def get_queryset(self):
#         queryset = Coupon.objects.filter(is_active=True)
#         return queryset


# urmi~~

class DeliveryAddressCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryAddressSerializer

    def post(self, request, *args, **kwargs):
        # request.data['user'] = request.user
        return super(DeliveryAddressCreateAPIView, self).post(request, *args, **kwargs)


class DeliveryAddressUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryAddressSerializer
    queryset = DeliveryAddress.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        return super(DeliveryAddressUpdateAPIView, self).put(request, *args, **kwargs)


class DeliveryAddressListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryAddressSerializer

    def get_queryset(self):
        queryset = DeliveryAddress.objects.filter(user=self.request.user)
        return queryset


class BillingAddressDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryAddressSerializer
    queryset = BillingAddress.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        return super(BillingAddressDeleteAPIView, self).delete(request, *args, **kwargs)


# class UserOrderListAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         queryset = Order.objects.filter(user=self.request.user).order_by('-ordered_date')
#         return queryset


# class VendorOrderListAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = VendorOrderSerializer
#
#     def get_queryset(self):
#         vendor = Vendor.objects.get(vendor_admin=self.request.user)
#         queryset = VendorOrder.objects.prefetch_related('order_items_vendor_order').filter(vendor=vendor)
#         return queryset


# class VendorOrderDetailsAPIView(RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = VendorOrderDetailSerializer
#     # lookup_field = 'oid'
#     # lookup_url_kwarg = 'oid'

#     def get_object(self):
#         # oid = self.kwargs['oid']
#         query = VendorOrder.objects.get(pk=self.kwargs['pk'])
#         return query


# class UserOrderDetailAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderItemSerializer
#     lookup_field = 'id'
#     lookup_url_kwarg = "id"

#     def get_queryset(self):
#         id = self.kwargs['id']
#         if id:
#             try:
#                 order = Order.objects.get(id=id)
#                 orderItem = OrderItem.objects.filter(order=order)
#                 return orderItem
#             except:
#                 raise ValidationError({"details": "Order Is Not Valid.!"})
#         return orderItem
