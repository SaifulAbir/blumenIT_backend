from rest_framework import serializers
from .models import *
from product.models import Product
from rest_framework.validators import UniqueTogetherValidator

# general Serializer start
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','thumbnail','title','price']

class noteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['notes']

# class CheckoutSerializer(serializers.Serializer):
#     notes = serializers.SerializerMethodField()
#     class Meta:
#         model = BillingAddress
#         fields = "__all__"

#     def get_notes(self, obj):
#         return noteSerializer()

class CheckoutSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, write_only=True)
    quantity = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    first_name = serializers.ListField(child=serializers.CharField(), write_only=True)
    last_name = serializers.ListField(child=serializers.CharField(), write_only=True)
    # address_type = serializers.ListField(child=ChoiceField(choices=BillingAddress.ADDRESS_CHOICES), write_only=True)
    class Meta:
        model = Order
        fields = ['id',
                'notes',
                'total_price',
                'coupon_status',
                'payment_type',
                'shipping_type',
                'product', 'quantity', 'first_name', 'last_name']
        # read_only_fields = ('ngo_username')

    def create(self, validated_data):
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        order_instance = Order.objects.create(**validated_data, user=self.context['request'].user)

        zip_object_order_items = zip(product, quantity)
        if zip_object_order_items:
            for p,q in zip_object_order_items:
                OrderItem.objects.create(order=order_instance, product=p, quantity=int(q), ordered=True, user=self.context['request'].user)

        zip_object_address = zip(first_name, last_name)
        if zip_object_address:
            for f_n,l_n in zip_object_address:
                CustomerAddress.objects.create(order=order_instance, first_name=f_n, last_name=l_n)
 
        return order_instance


# general Serializer end

class PaymentTypesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = [
                'id',
                'type_name',
                'note'
                ]

class ShippingTypesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingType
        fields = [
                'id',
                'type_name',
                'price'
                ]
# list Serializer end


# create Serializer start
# class PaymentTypeCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentType
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=PaymentType.objects.all(),
#                 fields=['type_name']
#             )
#         ]
#         fields = ['id', 'type_name', 'note']

# create Serializer end

# list Serializer start
class CartListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    subtotal = serializers.ReadOnlyField()
    class Meta:
        model = OrderItem
        fields = [
                'id',
                'quantity',
                'product',
                'subtotal'
                ]

#     def get_product(self, obj):
#         selected_product = Product.objects.filter(slug=obj.product.slug).distinct()
#         return ProductSerializer(selected_product, many=True).data