from rest_framework import serializers
from .models import *
from product.models import Product

# general Serializer start
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','thumbnail','title','price']

# general Serializer end

# create Serializer start


# create Serializer end

# list Serializer start
class CartListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = [
                'id',
                'quantity',
                'product'
                ]

    def get_product(self, obj):
        selected_product = Product.objects.filter(slug=obj.product.slug).distinct()
        return ProductSerializer(selected_product, many=True).data


# list Serializer end