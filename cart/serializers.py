from pyexpat import model
from attr import fields
from rest_framework import serializers
from .models import *
from product.models import Product
from rest_framework.validators import UniqueTogetherValidator

# general Serializer start


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'thumbnail', 'title', 'price', 'total_quantity']


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
    # ADDRESS_CHOICES = (
    #     ('Billing'),
    #     ('Shipping'),
    # )

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True)
    quantity = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)

    billing_first_name = serializers.CharField(write_only=True)
    billing_last_name = serializers.CharField(write_only=True)
    billing_country = serializers.CharField(write_only=True)
    billing_street_address = serializers.CharField(write_only=True)
    billing_city = serializers.CharField(write_only=True)
    billing_phone = serializers.CharField(write_only=True)
    billing_zip_code = serializers.CharField(write_only=True)
    billing_email = serializers.CharField(write_only=True)
    billing_default = serializers.BooleanField(write_only=True)

    shipping_first_name = serializers.CharField(write_only=True)
    shipping_last_name = serializers.CharField(write_only=True)
    shipping_country = serializers.CharField(write_only=True)
    shipping_street_address = serializers.CharField(write_only=True)
    shipping_city = serializers.CharField(write_only=True)
    shipping_zip_code = serializers.CharField(write_only=True)

    total_price = serializers.FloatField(write_only=True, required=True)
    discounted_price = serializers.FloatField(write_only=True, required=False)
    coupon = serializers.PrimaryKeyRelatedField(
        queryset=Coupon.objects.all(), many=False, write_only=True, required=False)
    coupon_status = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['id',
                  'notes',
                  'total_price',
                  'discounted_price',
                  'coupon',
                  'coupon_status',
                  'payment_type',
                  'product', 'quantity',
                  'billing_first_name', 'billing_last_name', 'billing_country', 'billing_street_address', 'billing_city', 'billing_phone',
                  'billing_zip_code', 'billing_email', 'billing_default',
                  'shipping_first_name', 'shipping_last_name', 'shipping_country', 'shipping_street_address', 'shipping_city', 'shipping_zip_code'
                  ]
        # read_only_fields = ('ngo_username')

    def create(self, validated_data):
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')

        billing_first_name = validated_data.pop('billing_first_name')
        billing_last_name = validated_data.pop('billing_last_name')
        billing_country = validated_data.pop('billing_country')
        billing_street_address = validated_data.pop('billing_street_address')
        billing_city = validated_data.pop('billing_city')
        billing_phone = validated_data.pop('billing_phone')
        billing_zip_code = validated_data.pop('billing_zip_code')
        billing_email = validated_data.pop('billing_email')
        billing_default = validated_data.pop('billing_default')

        shipping_first_name = validated_data.pop('shipping_first_name')
        shipping_last_name = validated_data.pop('shipping_last_name')
        shipping_country = validated_data.pop('shipping_country')
        shipping_street_address = validated_data.pop('shipping_street_address')
        shipping_city = validated_data.pop('shipping_city')
        shipping_zip_code = validated_data.pop('shipping_zip_code')

        order_instance = Order.objects.create(
            **validated_data, user=self.context['request'].user)

        zip_object_order_items = zip(product, quantity)
        if zip_object_order_items:
            for p, q in zip_object_order_items:
                OrderItem.objects.create(order=order_instance, product=p, quantity=int(
                    q), ordered=True, user=self.context['request'].user)
                # update product quantity
                product_current_quan = Product.objects.filter(slug=p.slug)[
                    0].total_quantity
                product_updated_quan = int(product_current_quan) - int(q)
                Product.objects.filter(slug=p.slug).update(
                    total_quantity=product_updated_quan)

                # update product sell_count
                product_sell_quan = Product.objects.filter(slug=p.slug)[
                    0].sell_count
                product_sell_quan += 1
                Product.objects.filter(slug=p.slug).update(
                    sell_count=product_sell_quan)

        CustomerAddress.objects.create(
            order=order_instance,
            address_type='Billing',
            first_name=billing_first_name,
            last_name=billing_last_name,
            country=billing_country,
            street_address=billing_street_address,
            city=billing_city,
            phone=billing_phone,
            zip_code=billing_zip_code,
            email=billing_email,
            default=billing_default
        )

        CustomerAddress.objects.create(
            order=order_instance,
            address_type='Shipping',
            first_name=shipping_first_name,
            last_name=shipping_last_name,
            country=shipping_country,
            street_address=shipping_street_address,
            city=shipping_city,
            zip_code=shipping_zip_code
        )

        return order_instance


class WishListDataSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = ['id', 'product']

    def get_product(self, obj):
        selected_product = Product.objects.filter(
            slug=obj.product.slug).distinct()
        return ProductSerializer(selected_product, many=True).data


class WishlistSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=False, write_only=True)


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


class ApplyCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'amount']

# class ActiveCouponListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Coupon
#         fields = '__all__'
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
