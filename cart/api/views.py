
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from cart.serializers import CartListSerializer, CheckoutSerializer, PaymentTypeCreateSerializer, PaymentTypesListSerializer, ShippingTypesListSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from user.models import User
from product.models import Product
from cart.models import Order, OrderItem, BillingAddress, PaymentType, ShippingType
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema



class AddToCartAPIView(APIView):

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        product_quantity = product.quantity
        user = User.objects.get(id = self.request.user.id)
        if product and product_quantity > 0:  #check for product and product quantity
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            # check order exist or not.
            if order_qs.exists():
                order_id = order_qs[0].id
                # check into order item table if exist then play with orderitem update
                order_item_check = OrderItem.objects.filter(product=product,ordered=False,order=order_id)
                if order_item_check:
                    order_item_current_quantity = order_item_check[0].quantity
                    increase_quantity = int(order_item_current_quantity) + 1
                    # if order item exist then increase item quantity till product quantity available
                    if increase_quantity <= product_quantity:
                        OrderItem_update = OrderItem.objects.filter(product=product,ordered=False,order=order_id).update(quantity = increase_quantity)
                        return Response({"status":"Order Item quantity increase!", "slug":order_qs[0].slug, "increase_quantity":increase_quantity,"user":self.request.user.id})
                    else:
                        return Response({"status":"Out Of stock!"})
                # check into order item table it orderItem doesn't exist then create a new row for orderitem
                else:
                    order = get_object_or_404(Order, slug=order_qs[0].slug)
                    order_item_created = OrderItem.objects.create(product=product,ordered=False,order=order,user=user)
                    return Response({"status":"Order Item added!", "slug":order_qs[0].slug,"user":self.request.user.id})
            # create a new order if order not exist.
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=user, ordered_date=ordered_date)
                order_item_created = OrderItem.objects.create(product=product,ordered=False,order=order,user=user)
                return Response({"status":"Order Created!", "slug":order.slug,"user":self.request.user.id})
        else:
            # raise ValidationError({"status":"Out Of stock!"})
            return Response({"status":"Out Of stock!"})

class RemoveFromCartAPIView(APIView):

    def post(self, request, slug, format=None):
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order_id = order_qs[0].id
            order_item_check = OrderItem.objects.filter(product=product,ordered=False,order=order_id)
            if order_item_check:
                order_item_check.delete()
                return Response({"status":"Item was removed from your cart."})
            else:
                return Response({"status":"Item was not in your cart."})
        else:
            return Response({"status":"Don't have an active order."})

class RemoveSingleItemFromCartAPIView(APIView):

    def post(self, request, slug, format=None):
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        product_quantity = product.quantity
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order_id = order_qs[0].id
            order_item_check = OrderItem.objects.filter(product=product,ordered=False,order=order_id)
            if order_item_check:
                order_item_current_quantity = order_item_check[0].quantity
                if order_item_current_quantity >  1:
                    decrease_quantity = int(order_item_current_quantity) - 1
                    OrderItem_update = OrderItem.objects.filter(product=product,ordered=False,order=order_id).update(quantity = decrease_quantity)
                    return Response({"status":"Order Item quantity decrease!", "slug":order_qs[0].slug, "decrease_quantity":decrease_quantity})
                else:
                    order_item_check.delete()
                    return Response({"status":"Item was not in your cart."})
            else:
                return Response({"status":"Item was not in your cart."})
        else:
            return Response({"status":slug})

class CartList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CartListSerializer
    lookup_field = 'uid'
    lookup_url_kwarg = "uid"
    def get_queryset(self):
        uid = self.kwargs['uid']
        user = User.objects.get(id = uid)
        query = OrderItem.objects.filter(user=user,ordered=False)
        return query

class CheckoutAPIView(APIView):
    def get(self, request):
        user = self.request.user.id
        order_item = OrderItem.objects.filter(user=user,ordered=False)
        cart_serializer = CartListSerializer(order_item, many=True)

        payment_types = PaymentType.objects.filter(status=True)
        payment_types_serializer = PaymentTypesListSerializer(payment_types, many=True)

        shipping_types = ShippingType.objects.filter(status=True)
        shipping_types_serializer = ShippingTypesListSerializer(shipping_types, many=True)

        return Response({"cart_data": cart_serializer.data, "payment_types": payment_types_serializer.data, "shipping_types": shipping_types_serializer.data})


    @swagger_auto_schema(request_body=CheckoutSerializer)
    def post(self, request):
        check_out_serializer = CheckoutSerializer(data=request.data)
        try:
            order = get_object_or_404(Order, user=self.request.user, ordered=False)

            if check_out_serializer.is_valid():
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                country = request.POST.get("country")
                street_address = request.POST.get("street_address")
                city = request.POST.get("city")
                zip_code = request.POST.get("zip_code")
                phone = request.POST.get("phone")
                email = request.POST.get("email")
                address_type = request.POST.get("address_type")
                default = request.POST.get("default")
                notes = request.POST.get("notes")

                if address_type == 'Billing':
                    billing_address = BillingAddress(
                        first_name=first_name,
                        last_name=last_name,
                        country=country,
                        street_address=street_address,
                        city=city,
                        zip_code=zip_code,
                        phone=phone,
                        email=email,
                        address_type='B',
                        default=default
                    )
                    billing_address.save()
                    order.billing_address = billing_address
                    if notes:
                        order.notes = notes
                    order.save()
                if address_type == 'Shipping':
                    shipping_address = BillingAddress(
                        first_name=first_name,
                        last_name=last_name,
                        country=country,
                        street_address=street_address,
                        city=city,
                        zip_code=zip_code,
                        phone=phone,
                        email=email,
                        address_type='S',
                        default=default
                    )
                    shipping_address.save()
                    order.shipping_address = shipping_address
                    if notes:
                        order.notes = notes
                    order.save()

                payment_type_slug = request.POST.get("payment_type_slug")
                payment_type = PaymentType.objects.get(slug = payment_type_slug)
                order.payment_type = payment_type
                order.save()

                # if payment_option == 'S':
                #     return redirect('core:payment', payment_option='stripe')
                # elif payment_option == 'P':
                #     return redirect('core:payment', payment_option='paypal')
                # else:
                #     messages.warning(
                #         self.request, "Invalid payment option select")
                #     return redirect('core:checkout')
                return Response({"status":"Data updated!"})
            else:
                return Response({"status": "Something went wrong!"})
        except ObjectDoesNotExist:
            return Response({"status": "You do not have an active order"})

class PaymentTypeCreateAPIView(CreateAPIView):
    serializer_class = PaymentTypeCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(PaymentTypeCreateAPIView, self).post(request, *args, **kwargs)

class TotalPriceAPIView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        # order = Order.objects.filter(user=self.request.user.id, ordered=False)
        order = Order.objects.get(user=self.request.user, ordered=False)
        # return Response({"order_total_price": str(order_qs)})
        amount = int(order.get_total_price())
        return Response({"order_total_price": amount})

class CheckQuantityAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        slug = request.POST.get("slug")
        quantity = int(request.POST.get("quantity"))
        product = get_object_or_404(Product, slug=slug)
        if product:
            available_quantity = product.quantity
            if quantity <= available_quantity:
                return Response({"status":'Available.'})
            else:
                return Response({"status":'Out of stock.'})
        else:
            return Response({"status":"Product not found"})