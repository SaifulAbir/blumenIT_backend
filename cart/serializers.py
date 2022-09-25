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
            **validated_data, user=self.context['request'].user, customer_profile=CustomerProfile.objects.get(user=self.context['request'].user))

        vendor_list = []
        zip_object_order_items = zip(product, quantity)
        if zip_object_order_items:
            for p, q in zip_object_order_items:
                # data add in vendor list
                vendor_list.append(p.vendor.id)

                # data store in orderIteam table
                OrderItem.objects.create(order=order_instance, product=p, quantity=int(
                    q), ordered=True, user=self.context['request'].user, vendor=p.vendor)
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

            print("vendor_list")
            print(vendor_list)

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

        # work with coupon start
        coupon_status = validated_data.pop('coupon_status')

        if coupon_status == True:
            coupon = validated_data.pop('coupon')
            coupon_id = Coupon.objects.get(id=coupon.id)
            user_id = User.objects.get(id=self.context['request'].user.id)
            coupon_obj = Coupon.objects.filter(id=coupon.id)
            check_in_use_coupon_record = UseRecordOfCoupon.objects.filter(
                coupon_id=coupon_obj[0].id, user_id=self.context['request'].user.id).exists()
            if check_in_use_coupon_record:
                pass
            else:
                UseRecordOfCoupon.objects.create(
                    coupon_id=coupon_id, user_id=user_id)
                number_of_uses = int(coupon_obj[0].number_of_uses)
                coupon_obj.update(number_of_uses=number_of_uses - 1)
                number_of_uses = Coupon.objects.get(
                    code=coupon_obj[0].code).number_of_uses
                if number_of_uses < 1:
                    coupon_obj.update(is_active=False)
        # work with coupon end

        return order_instance


class CheckoutDetailsAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = "__all__"


class CheckoutDetailsSerializer(serializers.ModelSerializer):
    payment_type_name = serializers.SerializerMethodField()
    billing_address = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        # fields = "__all__"
        fields = ['id', 'order_status', 'ordered_date',
                  'total_price', 'discounted_price', 'payment_type_name', 'billing_address', 'shipping_address']

    def get_payment_type_name(self, obj):
        payment_type_name = PaymentType.objects.filter(id=obj.payment_type.id)[
            0].type_name
        return payment_type_name

    def get_billing_address(self, obj):
        billing_address = CustomerAddress.objects.filter(
            order=obj, address_type='Billing')
        return CheckoutDetailsAddressSerializer(billing_address, many=True).data

    def get_shipping_address(self, obj):
        shipping_address = CustomerAddress.objects.filter(
            order=obj, address_type='Shipping')
        return CheckoutDetailsAddressSerializer(shipping_address, many=True).data


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


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ['id', 'user', 'first_name', 'last_name', 'country',
                  'street_address', 'city', 'phone', 'zip_code', 'email', 'title', 'default']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'ordered_date', 'order_status', 'total_price']

    # def get_order_items(self, obj):
    #     selected_order_items = OrderItem.objects.filter(
    #         user=obj.product.slug).distinct()
    #     return ProductSerializer(selected_product, many=True).data


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'subtotal']
