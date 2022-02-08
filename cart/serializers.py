from rest_framework import serializers
from .models import *
from product.models import Product

# general Serializer start
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','thumbnail','title','price']

class CheckoutSerializer(serializers.Serializer):
    notes = serializers.SerializerMethodField()
    class Meta:
        model = BillingAddress
        fields = "__all__"

# general Serializer end

# create Serializer start
class PaymentTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = "__all__"

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

    def get_product(self, obj):
        selected_product = Product.objects.filter(slug=obj.product.slug).distinct()
        return ProductSerializer(selected_product, many=True).data


# list Serializer end