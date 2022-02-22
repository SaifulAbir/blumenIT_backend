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
    ADDRESS_CHOICES = (
        ('Billing'),
        ('Shipping'),
    )

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, write_only=True)
    quantity = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    address_type = serializers.ListField(child=serializers.ChoiceField(choices=ADDRESS_CHOICES), write_only=True)
    first_name = serializers.ListField(child=serializers.CharField(), write_only=True)
    last_name = serializers.ListField(child=serializers.CharField(), write_only=True)
    country = serializers.ListField(child=serializers.CharField(), write_only=True)
    company_name = serializers.ListField(child=serializers.CharField(), write_only=True)
    street_address = serializers.ListField(child=serializers.CharField(), write_only=True)
    city = serializers.ListField(child=serializers.CharField(), write_only=True)
    zip_code = serializers.ListField(child=serializers.CharField(), write_only=True)
    phone = serializers.ListField(child=serializers.CharField(), write_only=True)
    email = serializers.ListField(child=serializers.CharField(), write_only=True)
    default = serializers.ListField(child=serializers.BooleanField(), write_only=True)
    class Meta:
        model = Order
        fields = ['id',
                'notes',
                'total_price',
                'coupon_status',
                'payment_type',
                'shipping_type',
                'product', 'quantity',
                'address_type', 'first_name', 'last_name', 'country', 'company_name',
                'street_address', 'city', 'zip_code', 'phone', 'email', 'default'
        ]
        # read_only_fields = ('ngo_username')

    def create(self, validated_data):
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')

        address_type = validated_data.pop('address_type')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        country = validated_data.pop('country')
        company_name = validated_data.pop('company_name')
        street_address = validated_data.pop('street_address')
        city = validated_data.pop('city')
        zip_code = validated_data.pop('zip_code')
        phone = validated_data.pop('phone')
        email = validated_data.pop('email')
        default = validated_data.pop('default')

        order_instance = Order.objects.create(**validated_data, user=self.context['request'].user)

        zip_object_order_items = zip(product, quantity)
        if zip_object_order_items:
            for p,q in zip_object_order_items:
                OrderItem.objects.create(order=order_instance, product=p, quantity=int(q), ordered=True, user=self.context['request'].user)
                # update product quantity
                product_current_quan = Product.objects.filter(slug = p.slug)[0].quantity
                product_updated_quan = int(product_current_quan) - int(q)
                Product.objects.filter(slug = p.slug).update(quantity=product_updated_quan)

                # update product sell_count
                product_sell_quan = Product.objects.filter(slug = p.slug)[0].sell_count
                product_sell_quan += 1
                Product.objects.filter(slug = p.slug).update(sell_count=product_sell_quan)

        zip_object_address = zip(address_type, first_name, last_name, country, company_name, street_address, city, zip_code, phone, email, default)
        if zip_object_address:
            for a_t, f_n, l_n, country, c_n, s_a, city, z_c, phone, e, d  in zip_object_address:
                CustomerAddress.objects.create(
                    order=order_instance,
                    address_type=a_t,
                    first_name=f_n,
                    last_name=l_n,
                    country=country,
                    company_name=c_n,
                    street_address=s_a,
                    city=city,
                    zip_code=z_c,
                    phone=phone,
                    email=e,
                    default=d,
                )

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