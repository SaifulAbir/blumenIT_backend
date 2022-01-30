
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
# from cart.serializers import AddToCartSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from user.models import User
from product.models import Product
from cart.models import Order, OrderItem
from django.utils import timezone



class AddToCartAPIView(APIView):

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        product_quantity = product.quantity
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
                        return Response({"status":"Order Item quantity increase!", "slug":order_qs[0].slug, "increase_quantity":increase_quantity})
                    else:
                        return Response({"status":"Out Of stock!"})
                # check into order item table it orderItem doesn't exist then create a new row for orderitem
                else:
                    order = get_object_or_404(Order, slug=order_qs[0].slug)
                    order_item_created = OrderItem.objects.create(product=product,ordered=False,order=order)
                    return Response({"status":"Order Item added!", "slug":order_qs[0].slug})
            # create a new order if order not exist.
            else:
                ordered_date = timezone.now()
                user = User.objects.get(id = self.request.user.id)
                order = Order.objects.create(user=user, ordered_date=ordered_date)
                order_item_created = OrderItem.objects.create(product=product,ordered=False,order=order)
                return Response({"status":"Order Created!", "slug":order.slug})
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
            order_item_current_quantity = order_item_check[0].quantity
            if order_item_current_quantity >  1:
                decrease_quantity = int(order_item_current_quantity) - 1
                OrderItem_update = OrderItem.objects.filter(product=product,ordered=False,order=order_id).update(quantity = decrease_quantity)
                return Response({"status":"Order Item quantity decrease!", "slug":order_qs[0].slug, "decrease_quantity":decrease_quantity})
            else:
                order_item_check.delete()
                return Response({"status":"Item was not in your cart."})
        else:
            return Response({"status":slug})