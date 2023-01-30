from django.utils import timezone
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from product.serializers import DiscountTypeSerializer
from cart.serializers import CheckoutDetailsSerializer, CheckoutSerializer, \
     PaymentTypesListSerializer, ApplyCouponSerializer, DeliveryAddressSerializer, ShippingClassDataSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Product, DiscountTypes, ShippingClass
from cart.models import BillingAddress, Order, PaymentType, Coupon, UseRecordOfCoupon, Wishlist, \
    DeliveryAddress
from user.models import User
from django.db.models import Q


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


class CheckoutDetailsAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckoutDetailsSerializer
    lookup_field = 'o_id'
    lookup_url_kwarg = 'o_id'

    def get_object(self):
        o_id = self.kwargs['o_id']
        try:
            query = Order.objects.get(id=o_id)
            return query
        except:
            raise ValidationError(
                {"details": "Order doesn't exist."})


class WishlistAddRemoveAPIView(APIView):
    queryset = Wishlist.objects.all()

    def post(self, request, product_id):
        if self.request.user.is_customer == True:

            user_id = self.request.user
            product_id = self.kwargs['product_id']
            product = Product.objects.get(id=product_id)
            wishlist_data_exist = Wishlist.objects.filter(Q(user=user_id), Q(product=product_id)).exists()
            if wishlist_data_exist:
                Wishlist.objects.filter(Q(user=user_id), Q(product=product_id)).delete()
                return Response({"msg": "wishlist updated!"})
            else:
                Wishlist.objects.create(user=user_id, product=product, is_active=True)
                return Response({"msg": "wishlist created!"})
        else:
            raise ValidationError(
                {"msg": 'You are not an User!'})


class DeliveryAddressCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryAddressSerializer

    def post(self, request, *args, **kwargs):
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
        queryset = DeliveryAddress.objects.filter(user=self.request.user, is_active=True).order_by('-created_at')
        return queryset


class BillingAddressDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryAddressSerializer
    queryset = BillingAddress.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        return super(BillingAddressDeleteAPIView, self).delete(request, *args, **kwargs)


class ShippingClassDataAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShippingClassDataSerializer

    def get_queryset(self):
        queryset = ShippingClass.objects.filter(is_active=True).order_by('-created_at')
        return queryset