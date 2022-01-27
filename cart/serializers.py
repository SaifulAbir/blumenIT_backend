from rest_framework import serializers
from .models import *


# create Serializer start
class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        # fields = []
        # read_only_fields = ('user')


    # def create(self, validated_data):
    #     slug = validated_data['slug']
    #     product = get_object_or_404(Product, slug=slug)
        # ordered_date = timezone.now()
        # order = Order.objects.create(user=self.context['request'].user.id, ordered_date=ordered_date)
        # order_item, created = OrderItem.objects.get_or_create(product=product,ordered=False, order=order)
        # order_qs = Order.objects.filter(user=self.context['request'].user.id, ordered=False)

        # ordered_date = timezone.now()
        # order = Order.objects.create(user=self.context['request'].user.id, ordered_date=ordered_date)
        # print(order)
        # order.items.add(order_item)

        # order_qs = Order.objects.filter(user=self.context['request'].user.id, ordered=False)
        # if order_qs.exists():
        #     print("if")
        # else:
        #     print("else")

        # return created
# create Serializer end