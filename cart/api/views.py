
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, DestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from product.serializers import DiscountTypeSerializer
from cart.serializers import BillingAddressSerializer, CheckoutDetailsSerializer, CheckoutSerializer, \
    OrderItemSerializer, OrderSerializer, PaymentTypesListSerializer, WishlistSerializer, WishListDataSerializer, \
    ApplyCouponSerializer, CouponSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from user.models import User
from product.models import Product, DiscountTypes
from cart.models import BillingAddress, Order, OrderItem, PaymentType, Coupon, UseRecordOfCoupon, Wishlist, VendorOrder
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone

from vendor.models import Vendor



class CouponCreateAPIView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = CouponSerializer

    def post(self, request):
        coupon = CouponSerializer(data=request.data)

        if Coupon.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')

        if coupon.is_valid():
            coupon.save()
            return Response(coupon.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CouponListAPIView(ListAPIView):

    queryset = Coupon.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CouponSerializer

class CouponUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        return super(CouponUpdateAPIView, self).put(request, *args, **kwargs)

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


# class PaymentMethodsAPIView(ListAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = PaymentTypesListSerializer

#     def get_queryset(self):
#         queryset = PaymentType.objects.filter(status=True)
#         return queryset

# class ApplyCouponAPIView(RetrieveUpdateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = ApplyCouponSerializer
#     lookup_field = 'code'
#     lookup_url_kwarg = "code"

#     def get_queryset(self):
#         code = self.kwargs['code']
#         query = Coupon.objects.filter(code=code, is_active=True)
#         return query

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)


# class ApplyCouponAPIView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = ApplyCouponSerializer
#     lookup_field = 'code'
#     lookup_url_kwarg = 'code'

#     def get(self, request, code, uid):
#         # try:
#         code = self.kwargs['code']
#         uid = self.kwargs['uid']

#         # check coupon code exist or not
#         code_exist = Coupon.objects.filter(code=code, is_active=True).exists()
#         if code_exist:
#             coupon_obj = Coupon.objects.filter(code=code)
#             start_date_time = coupon_obj[0].start_time
#             end_date_time = coupon_obj[0].end_time

#             current_time = timezone.now()

#             # date comparison with current date
#             if current_time > start_date_time and current_time < end_date_time:
#                 # check number of uses of coupon
#                 number_of_uses = int(coupon_obj[0].number_of_uses)
#                 print(number_of_uses)
#                 if number_of_uses > 0:
#                     # check if this user already used this coupon
#                     user = User.objects.filter(id=uid).exists()
#                     if user:
#                         user_obj = User.objects.filter(id=uid)
#                         check_in_use_coupon_record = UseRecordOfCoupon.objects.filter(
#                             coupon_id=coupon_obj[0].id, user_id=user_obj[0].id).exists()
#                         if check_in_use_coupon_record:
#                             return Response({"status": "You already used this coupon!"})
#                         else:
#                             #     coupon_id = Coupon.objects.get(
#                             #         code=coupon_obj[0].code)
#                             #     user_id = User.objects.get(id=uid)
#                             #     # print(type(coupon_id))
#                             #     UseRecordOfCoupon.objects.create(
#                             #         coupon_id=coupon_id, user_id=user_id)
#                             #     coupon_obj.update(
#                             #         number_of_uses=number_of_uses - 1)
#                             #     number_of_uses = Coupon.objects.get(
#                             #         code=coupon_obj[0].code).number_of_uses
#                             #     if number_of_uses < 1:
#                             #         coupon_obj.update(is_active=False)

#                             return Response({"status": "Authentic coupon.", "amount": coupon_obj[0].amount, "coupon_id": coupon_obj[0].id})
#                     else:
#                         return Response({"status": "User doesn't exist!"})

#                 else:
#                     return Response({"status": "Invalid coupon!"})

#             else:
#                 if current_time > end_date_time:
#                     coupon_obj.update(is_active=False)
#                 return Response({"status": "Invalid coupon!"})

#             # if code_status == True:
#             #     return Response({"data": code_status})
#             # else:
#             #     return Response({"status": "Invalid coupon!"})

#             # return Response({"data": current_time, "start_date_time": start_date_time })
#         else:
#             return Response({"status": "Invalid coupon!"})
            # return Response({"status": "Code Invalid, Coupon does not exist!"})
        # except:
        #     return Response({"status": "Something went wrong, contact with developer!"})

        # return Response({"data": "code"})


# class WishListAPIView(ListCreateAPIView):
# class WishListAPIView(APIView):
#     permission_classes = (AllowAny,)

#     def get(self, request):
#         user = self.request.user.id
#         wishlist = Wishlist.objects.filter(user=user, is_active=True)
#         wishlist_serializer_data = WishListDataSerializer(wishlist, many=True)
#         return Response({"wishlist": wishlist_serializer_data.data})

#     def post(self, request):
#         wishlist_serializer = WishlistSerializer(data=request.data)
#         if wishlist_serializer.is_valid():
#             product = request.POST.get("product")
#             if product:
#                 whishlist_exc = Wishlist.objects.filter(user=User.objects.get(
#                     id=self.request.user.id), product=Product.objects.get(id=product), is_active=True)
#                 if not whishlist_exc:
#                     wishlist = Wishlist(
#                         user=User.objects.get(id=self.request.user.id),
#                         product=Product.objects.get(id=product)
#                     )
#                     wishlist.save()
#                 else:
#                     return Response({"status": "Already exist!"})
#         return Response({"status": "Data uploaded!"})


# class WishlistDeleteAPIView(DestroyAPIView):
#     serializer_class = WishListDataSerializer

#     def get_queryset(self):
#         queryset = Wishlist.objects.filter(id=self.kwargs['id'])
#         return queryset

# class CheckoutAPIView(APIView):
    # def get(self, request):
    #     user = self.request.user.id
    #     # order_item = OrderItem.objects.filter(user=user,ordered=False)
    #     # cart_serializer = CartListSerializer(order_item, many=True)

    #     payment_types = PaymentType.objects.filter(status=True)
    #     payment_types_serializer = PaymentTypesListSerializer(payment_types, many=True)

    #     shipping_types = ShippingType.objects.filter(status=True)
    #     shipping_types_serializer = ShippingTypesListSerializer(shipping_types, many=True)

    #     return Response({"payment_types": payment_types_serializer.data, "shipping_types": shipping_types_serializer.data})
    #     # return Response({"cart_data": cart_serializer.data, "payment_types": payment_types_serializer.data, "shipping_types": shipping_types_serializer.data})

    # @swagger_auto_schema(request_body=CheckoutSerializer)
    # def post(self, request):
    #     check_out_serializer = CheckoutSerializer(data=request.data)
    #     try:
    #         order = get_object_or_404(Order, user=self.request.user, ordered=False)

    #         if check_out_serializer.is_valid():
    #             first_name = request.POST.get("first_name")
    #             last_name = request.POST.get("last_name")
    #             country = request.POST.get("country")
    #             street_address = request.POST.get("street_address")
    #             city = request.POST.get("city")
    #             zip_code = request.POST.get("zip_code")
    #             phone = request.POST.get("phone")
    #             email = request.POST.get("email")
    #             address_type = request.POST.get("address_type")
    #             default = request.POST.get("default")
    #             notes = request.POST.get("notes")

    #             if address_type == 'Billing':
    #                 billing_address = BillingAddress(
    #                     first_name=first_name,
    #                     last_name=last_name,
    #                     country=country,
    #                     street_address=street_address,
    #                     city=city,
    #                     zip_code=zip_code,
    #                     phone=phone,
    #                     email=email,
    #                     address_type='B',
    #                     default=default
    #                 )
    #                 billing_address.save()
    #                 order.billing_address = billing_address
    #                 if notes:
    #                     order.notes = notes
    #                 order.save()
    #             if address_type == 'Shipping':
    #                 shipping_address = BillingAddress(
    #                     first_name=first_name,
    #                     last_name=last_name,
    #                     country=country,
    #                     street_address=street_address,
    #                     city=city,
    #                     zip_code=zip_code,
    #                     phone=phone,
    #                     email=email,
    #                     address_type='S',
    #                     default=default
    #                 )
    #                 shipping_address.save()
    #                 order.shipping_address = shipping_address
    #                 if notes:
    #                     order.notes = notes
    #                 order.save()

    #             payment_type_slug = request.POST.get("payment_type_slug")
    #             payment_type = PaymentType.objects.get(slug = payment_type_slug)
    #             order.payment_type = payment_type
    #             order.save()

    #             # if payment_option == 'S':
    #             #     return redirect('core:payment', payment_option='stripe')
    #             # elif payment_option == 'P':
    #             #     return redirect('core:payment', payment_option='paypal')
    #             # else:
    #             #     messages.warning(
    #             #         self.request, "Invalid payment option select")
    #             #     return redirect('core:checkout')
    #             return Response({"status":"Data updated!"})
    #         else:
    #             return Response({"status": "Something went wrong!"})
    #     except ObjectDoesNotExist:
    #         return Response({"status": "You do not have an active order"})


# class AddToCartAPIView(APIView):

#     def post(self, request, *args, **kwargs):
#         slug = self.kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         product_quantity = product.quantity
#         user = User.objects.get(id = self.request.user.id)
#         if product and product_quantity > 0:  #check for product and product quantity
#             order_qs = Order.objects.filter(user=self.request.user, ordered=False)
#             # check order exist or not.
#             if order_qs.exists():
#                 order_id = order_qs[0].id
#                 # check into order item table if exist then play with orderitem update
#                 order_item_check = OrderItem.objects.filter(product=product,ordered=False,order=order_id)
#                 if order_item_check:
#                     order_item_current_quantity = order_item_check[0].quantity
#                     increase_quantity = int(order_item_current_quantity) + 1
#                     # if order item exist then increase item quantity till product quantity available
#                     if increase_quantity <= product_quantity:
#                         OrderItem_update = OrderItem.objects.filter(product=product,ordered=False,order=order_id).update(quantity = increase_quantity)
#                         return Response({"status":"Order Item quantity increase!", "slug":order_qs[0].slug, "increase_quantity":increase_quantity,"user":self.request.user.id})
#                     else:
#                         return Response({"status":"Out Of stock!"})
#                 # check into order item table it orderItem doesn't exist then create a new row for orderitem
#                 else:
#                     order = get_object_or_404(Order, slug=order_qs[0].slug)
#                     order_item_created = OrderItem.objects.create(product=product,ordered=False,order=order,user=user)
#                     return Response({"status":"Order Item added!", "slug":order_qs[0].slug,"user":self.request.user.id})
#             # create a new order if order not exist.
#             else:
#                 ordered_date = timezone.now()
#                 order = Order.objects.create(user=user, ordered_date=ordered_date)
#                 order_item_created = OrderItem.objects.create(product=product,ordered=False,order=order,user=user)
#                 return Response({"status":"Order Created!", "slug":order.slug,"user":self.request.user.id})
#         else:
#             # raise ValidationError({"status":"Out Of stock!"})
#             return Response({"status":"Out Of stock!"})

# class RemoveFromCartAPIView(APIView):

#     def post(self, request, slug, format=None):
#         slug = self.kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         order_qs = Order.objects.filter(user=self.request.user, ordered=False)
#         if order_qs.exists():
#             order_id = order_qs[0].id
#             order_item_check = OrderItem.objects.filter(product=product,ordered=False,order=order_id)
#             if order_item_check:
#                 order_item_check.delete()
#                 return Response({"status":"Item was removed from your cart."})
#             else:
#                 return Response({"status":"Item was not in your cart."})
#         else:
#             return Response({"status":"Don't have an active order."})

# class RemoveSingleItemFromCartAPIView(APIView):

#     def post(self, request, slug, format=None):
#         slug = self.kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         product_quantity = product.quantity
#         order_qs = Order.objects.filter(user=self.request.user, ordered=False)
#         if order_qs.exists():
#             order_id = order_qs[0].id
#             order_item_check = OrderItem.objects.filter(product=product,ordered=False,order=order_id)
#             if order_item_check:
#                 order_item_current_quantity = order_item_check[0].quantity
#                 if order_item_current_quantity >  1:
#                     decrease_quantity = int(order_item_current_quantity) - 1
#                     OrderItem_update = OrderItem.objects.filter(product=product,ordered=False,order=order_id).update(quantity = decrease_quantity)
#                     return Response({"status":"Order Item quantity decrease!", "slug":order_qs[0].slug, "decrease_quantity":decrease_quantity})
#                 else:
#                     order_item_check.delete()
#                     return Response({"status":"Item was not in your cart."})
#             else:
#                 return Response({"status":"Item was not in your cart."})
#         else:
#             return Response({"status":slug})

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

# class TotalPriceAPIView(APIView):
#     # permission_classes = (AllowAny,)

#     def get(self, request):
#         # order = Order.objects.filter(user=self.request.user.id, ordered=False)
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         # return Response({"order_total_price": str(order_qs)})
#         amount = int(order.get_total_price())
#         return Response({"order_total_price": amount})

# class CheckQuantityAPIView(APIView):
#     permission_classes = (AllowAny,)
#     def post(self, request):
#         slug = request.POST.get("slug")
#         quantity = int(request.POST.get("quantity"))
#         product = get_object_or_404(Product, slug=slug)
#         if product:
#             available_quantity = product.quantity
#             if quantity <= available_quantity:
#                 return Response({"status":'Available.'})
#             else:
#                 return Response({"status":'Out of stock.'})
#         else:
#             return Response({"status":"Product not found"})

# class ActiveCouponlistView(ListAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = ActiveCouponListSerializer
#     def get_queryset(self):
#         queryset = Coupon.objects.filter(is_active=True)
#         return queryset


# urmi~~

# class BillingAddressCreateAPIView(CreateAPIView):
#     serializer_class = BillingAddressSerializer

#     def post(self, request, *args, **kwargs):
#         return super(BillingAddressCreateAPIView, self).post(request, *args, **kwargs)


# class BillingAddressUpdateAPIView(RetrieveUpdateAPIView):
#     serializer_class = BillingAddressSerializer
#     queryset = BillingAddress.objects.all()
#     lookup_field = 'id'
#     lookup_url_kwarg = "id"

#     def put(self, request, *args, **kwargs):
#         return super(BillingAddressUpdateAPIView, self).put(request, *args, **kwargs)


# class BillingAddressListAPIView(ListAPIView):
#     serializer_class = BillingAddressSerializer

#     def get_queryset(self):
#         queryset = BillingAddress.objects.filter(user=self.request.user)
#         return queryset


# class BillingAddressDeleteAPIView(DestroyAPIView):
#     serializer_class = BillingAddressSerializer
#     queryset = BillingAddress.objects.all()
#     lookup_field = 'id'
#     lookup_url_kwarg = "id"

#     def delete(self, request, *args, **kwargs):
#         return super(BillingAddressDeleteAPIView, self).delete(request, *args, **kwargs)


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
