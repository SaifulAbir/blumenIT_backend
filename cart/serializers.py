from pickle import TRUE
from pyexpat import model
from attr import fields
from rest_framework import serializers
from .models import *
from product.models import Product, Inventory, Specification
from product.serializers import SpecificationSerializer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError


class CouponSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Coupon
        read_only_field = ['id']
        fields = [  'id',
                    'code',
                    'coupon_type',
                    'amount',
                    'discount_type',
                    'number_of_uses',
                    'start_time',
                    'end_time',
                    'min_shopping',
                    'is_active'
                ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'thumbnail', 'title', 'price', 'total_quantity']


class noteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['notes']


class ProductCombinationForCheckoutSerializer(serializers.ModelSerializer):

    product = serializers.IntegerField(write_only=True, required=True)
    quantity = serializers.IntegerField(write_only=True, required=True)
    price = serializers.DecimalField(
        max_digits=255, decimal_places=2, required=True)
    product_attribute = serializers.IntegerField(
        write_only=True, required=False)
    product_attribute_value = serializers.CharField(
        write_only=True, required=False)
    variant_type = serializers.IntegerField(write_only=True, required=False)
    variant_value = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = OrderItem
        fields = ['id',
                  'product',
                  'quantity',
                  'price',
                  'product_attribute',
                  'product_attribute_value',
                  'variant_type',
                  'variant_value'
                  ]


class CheckoutDetailsOrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title',read_only=True)
    product_sku = serializers.CharField(source='product.sku',read_only=True)
    product_thumb = serializers.ImageField(source='product.thumbnail',read_only=True)
    product_price = serializers.SerializerMethodField()
    product_specification = serializers.SerializerMethodField('get_product_specification')

    class Meta:
        model = OrderItem
        fields = ['id', 'product_title', 'product_thumb', 'quantity', 'product_price', 'product_sku', 'product_specification']

    def get_product_price(self, obj):
        product_price = Product.objects.filter(id=obj.product.id)[
            0].price
        return product_price

    def get_product_specification(self, obj):
        queryset = Specification.objects.filter(product=obj.product.id, is_active = True)
        serializer = SpecificationSerializer(instance=queryset, many=True)
        return serializer.data


class CheckoutDetailsDeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['id', 'user', 'name', 'address', 'phone',
                  'email', 'zip_code', 'country', 'city', 'state']


class CheckoutDetailsSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField('get_order_items')
    sub_total = serializers.SerializerMethodField('get_sub_total')
    delivery_address = serializers.SerializerMethodField('get_delivery_address')
    payment_title = serializers.CharField(source='payment_type.type_name',read_only=True)
    user_email = serializers.EmailField(source='user.email',read_only=True)
    user_phone = serializers.CharField(source='user.phone',read_only=True)
    product_price = serializers.SerializerMethodField('get_product_price')
    total_price = serializers.SerializerMethodField('get_total_price')
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'user_phone', 'order_id', 'order_date', 'delivery_date', 'order_status', 'order_items', 'delivery_address', 'payment_type',
        'payment_title', 'product_price', 'coupon_discount_amount', 'sub_total', 'shipping_cost', 'total_price']

    def get_order_items(self, obj):
        queryset = OrderItem.objects.filter(order=obj) 
        serializer = CheckoutDetailsOrderItemSerializer(instance=queryset, many=True, context={'request': self.context['request']})
        return serializer.data

    def get_delivery_address(self, obj):
        try:
            if obj.delivery_address:
                queryset = DeliveryAddress.objects.filter(id=obj.delivery_address.id)
                serializer = CheckoutDetailsDeliveryAddressSerializer(instance=queryset, many=True)
                return serializer.data
            else:
                return ''
        except:
            return ''

    def get_sub_total(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        prices = []
        for order_item in order_items:
            price = order_item.unit_price
            quantity = order_item.quantity
            t_price = float(price) * float(quantity)
            prices.append(t_price)
        sub_total = sum(prices)
        return sub_total

    def get_product_price(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        prices = []
        for order_item in order_items:
            price = order_item.unit_price
            prices.append(price)
        product_price_total = sum(prices)
        return product_price_total

    def get_total_price(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        prices = []
        total_price = 0
        for order_item in order_items:
            price = order_item.unit_price
            quantity = order_item.quantity
            t_price = float(price) * float(quantity)
            prices.append(t_price)
        sub_total = sum(prices)
        if sub_total:
            total_price += sub_total

        shipping_cost = obj.shipping_cost
        if shipping_cost:
            total_price += shipping_cost

        coupon_discount_amount = obj.coupon_discount_amount
        if coupon_discount_amount:
            total_price -= coupon_discount_amount
        return total_price



class WishlistSerializer(serializers.Serializer):
    # product = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(), many=False, write_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'is_active']


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


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['id', 'user', 'name', 'address', 'phone',
                  'email', 'zip_code', 'country', 'city', 'state']

    def create(self, validated_data):
        address_instance = DeliveryAddress.objects.create(**validated_data, user=self.context['request'].user)
        return address_instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_id', 'product_count', 'order_date', 'order_status', 'total_price']

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


# class VendorOrderSerializer(serializers.ModelSerializer):
#     customer_profile = CustomerProfileSerializer()
#     order = OrderSerializer()
#     # order_items_vendor_order = OrderItemSerializer(many=True)
#
#     class Meta:
#         model = VendorOrder
#         fields = ['id', 'order', 'user', 'customer_profile', 'vendor_order_id', 'ordered_date', 'ordered', 'received',
#                   'refund_requested', 'refund_granted', 'shipping_type', 'order_status', 'vendor', 'order_items_vendor_order']


# class VendorOrderDetailSerializer(serializers.ModelSerializer):
#     customer_profile = CustomerProfileSerializer()
#     order = OrderSerializer()
#     order_items_vendor_order = OrderItemSerializer(many=True)
#     vendor = VendorDetailSerializer()
#     class Meta:
#         model = VendorOrder
#         fields = ['id', 'order', 'user', 'customer_profile', 'vendor_order_id', 'ordered_date', 'ordered', 'received',
#                   'refund_requested', 'refund_granted', 'shipping_type', 'order_status', 'vendor', 'order_items_vendor_order']

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

# class CheckoutSerializer(serializers.Serializer):
#     notes = serializers.SerializerMethodField()
#     class Meta:
#         model = BillingAddress
#         fields = "__all__"

#     def get_notes(self, obj):
#         return noteSerializer()



# class CheckoutSerializer(serializers.ModelSerializer):
#
#     order_items = ProductCombinationForCheckoutSerializer(
#         many=True, required=False)
#
#     billing_first_name = serializers.CharField(write_only=True)
#     billing_last_name = serializers.CharField(write_only=True)
#     billing_country = serializers.CharField(write_only=True)
#     billing_street_address = serializers.CharField(write_only=True)
#     billing_city = serializers.CharField(write_only=True)
#     billing_phone = serializers.CharField(write_only=True)
#     billing_zip_code = serializers.CharField(write_only=True)
#     billing_email = serializers.CharField(write_only=True)
#     billing_default = serializers.BooleanField(write_only=True)
#
#     shipping_first_name = serializers.CharField(write_only=True)
#     shipping_last_name = serializers.CharField(write_only=True)
#     shipping_country = serializers.CharField(write_only=True)
#     shipping_street_address = serializers.CharField(write_only=True)
#     shipping_city = serializers.CharField(write_only=True)
#     shipping_phone = serializers.CharField(write_only=True)
#     shipping_zip_code = serializers.CharField(write_only=True)
#     shipping_email = serializers.CharField(write_only=True)
#
#     total_price = serializers.FloatField(write_only=True, required=True)
#     discounted_price = serializers.FloatField(write_only=True, required=False)
#     coupon = serializers.PrimaryKeyRelatedField(
#         queryset=Coupon.objects.all(), many=False, write_only=True, required=False)
#     coupon_status = serializers.BooleanField(write_only=True, required=False)
#
#     class Meta:
#         model = Order
#         fields = ['id',
#                   'notes',
#                   'total_price',
#                   'discounted_price',
#                   'coupon',
#                   'coupon_status',
#                   'payment_type',
#                   'order_items',
#                   'billing_first_name', 'billing_last_name', 'billing_country', 'billing_street_address', 'billing_city', 'billing_phone',
#                   'billing_zip_code', 'billing_email', 'billing_default',
#                   'shipping_first_name', 'shipping_last_name', 'shipping_country', 'shipping_street_address', 'shipping_city', 'shipping_phone', 'shipping_zip_code', 'shipping_email',
#                   ]
#         # read_only_fields = ('ngo_username')
#
#     def create(self, validated_data):
#
#         billing_first_name = validated_data.pop('billing_first_name')
#         billing_last_name = validated_data.pop('billing_last_name')
#         billing_country = validated_data.pop('billing_country')
#         billing_street_address = validated_data.pop('billing_street_address')
#         billing_city = validated_data.pop('billing_city')
#         billing_phone = validated_data.pop('billing_phone')
#         billing_zip_code = validated_data.pop('billing_zip_code')
#         billing_email = validated_data.pop('billing_email')
#         billing_default = validated_data.pop('billing_default')
#
#         shipping_first_name = validated_data.pop('shipping_first_name')
#         shipping_last_name = validated_data.pop('shipping_last_name')
#         shipping_country = validated_data.pop('shipping_country')
#         shipping_street_address = validated_data.pop('shipping_street_address')
#         shipping_city = validated_data.pop('shipping_city')
#         shipping_phone = validated_data.pop('shipping_phone')
#         shipping_zip_code = validated_data.pop('shipping_zip_code')
#         shipping_email = validated_data.pop('shipping_email')
#
#         try:
#             order_items = validated_data.pop('order_items')
#         except:
#             order_items = ''
#
#         order_instance = Order.objects.create(
#             **validated_data, user=self.context['request'].user, customer_profile=CustomerProfile.objects.get(user=self.context['request'].user))
#
#         if order_items:
#             vendor_list = []
#             count = 0
#
#             for order_item in order_items:
#                 product = order_item['product']
#                 quantity = order_item['quantity']
#                 price = order_item['price']
#                 try:
#                     product_attribute = order_item['product_attribute']
#                 except:
#                     product_attribute = 0
#                 try:
#                     product_attribute_value = order_item['product_attribute_value']
#                 except:
#                     product_attribute_value = ''
#                 try:
#                     variant_type = order_item['variant_type']
#                 except:
#                     variant_type = 0
#                 try:
#                     variant_value = order_item['variant_value']
#                 except:
#                     variant_value = ''
#
#                 product_obj = Product.objects.get(id=product)
#
#                 vendor_id = product_obj.vendor.id
#                 if vendor_id not in vendor_list:
#                     vendor_list.append(vendor_id)
#                     print(vendor_list)
#                     # data store in vendor order table
#                     VendorOrder.objects.create(order=order_instance, user=self.context['request'].user, vendor=Vendor.objects.get(
#                         id=vendor_id), customer_profile=CustomerProfile.objects.get(user=self.context['request'].user))
#
#                 # product sell count update
#                 count += 1
#                 product_sell_quan = Product.objects.filter(
#                     slug=product_obj.slug)[0].sell_count
#                 product_sell_quan += 1
#                 Product.objects.filter(slug=product_obj.slug).update(
#                     sell_count=product_sell_quan)
#
#                 # data store in orderIteam table
#                 vendor_order = VendorOrder.objects.get(
#                     vendor=product_obj.vendor, order=order_instance)
#                 order_item_instance = OrderItem.objects.create(order=order_instance, product=product_obj, quantity=int(
#                     quantity), ordered=True, user=self.context['request'].user, vendor=product_obj.vendor, vendor_order=vendor_order)
#
#                 # data store in OrderItemCombination table
#                 if product_attribute != 0:
#                     order_item_combination_instance = OrderItemCombination.objects.create(
#                         product=product_obj, order=order_instance, orderItem=order_item_instance, product_attribute=ProductAttributes.objects.get(id=product_attribute), product_attribute_value=product_attribute_value, product_attribute_price=price)
#                 if variant_type != 0:
#                     OrderItemCombination.objects.filter(id=order_item_combination_instance.id).update(
#                         variant_type=VariantType.objects.get(id=variant_type), variant_value=variant_value, variant_price=price)
#
#             Order.objects.filter(id=order_instance.id).update(
#                 product_count=count)
#
#         # vendor_list = []
#
#         # if product:
#         #     for p in product:
#         #         # data add in vendor order table
#         #         if p.vendor.id not in vendor_list:
#         #             vendor_list.append(p.vendor.id)
#
#         #     if len(vendor_list) > 0:
#         #         for v in vendor_list:
#         #             # data store in vendor order table
#         #             VendorOrder.objects.create(order=order_instance, user=self.context['request'].user, vendor=Vendor.objects.get(id=v), customer_profile=CustomerProfile.objects.get(
#         #                 user=self.context['request'].user))
#
#         # count = 0
#         # zip_object_order_items = zip(
#         #     product, quantity, product_attribute, product_attribute_value, variant_type, variant_value, variant_price)
#         # if zip_object_order_items:
#         #     for p, q, p_a, p_a_v, v_t, v_v, v_p in zip_object_order_items:
#         #         # increase product count
#         #         count += 1
#         #         vendor_order = VendorOrder.objects.get(
#         #             vendor=p.vendor, order=order_instance)
#
#         #         # data store in orderIteam table
#         #         order_item_instance = OrderItem.objects.create(order=order_instance, product=p, quantity=int(
#         #             q), ordered=True, user=self.context['request'].user, vendor=p.vendor, vendor_order=vendor_order)
#
#         #         # data store in OrderItemCombination table
#         #         if p_a != 0:
#         #             order_item_combination_instance = OrderItemCombination.objects.create(
#         #                 product=p, order=order_instance, orderItem=order_item_instance, product_attribute=ProductAttributes.objects.get(id=p_a), product_attribute_value=p_a_v, variant_type=VariantType.objects.get(id=v_t), variant_value=v_v, variant_price=v_p, variant_ordered_quantity=int(q))
#
#         #         # update product quantity
#         #         product_current_quan = Product.objects.filter(slug=p.slug)[
#         #             0].total_quantity
#         #         product_updated_quan = int(product_current_quan) - int(q)
#         #         Product.objects.filter(slug=p.slug).update(
#         #             total_quantity=product_updated_quan)
#
#         #         # update product sell_count
#         #         product_sell_quan = Product.objects.filter(slug=p.slug)[
#         #             0].sell_count
#         #         product_sell_quan += 1
#         #         Product.objects.filter(slug=p.slug).update(
#         #             sell_count=product_sell_quan)
#
#         #     Order.objects.filter(id=order_instance.id).update(
#         #         product_count=count)
#         # else:
#         #     print('else')
#
#         CustomerAddress.objects.create(
#             order=order_instance,
#             address_type='Billing',
#             first_name=billing_first_name,
#             last_name=billing_last_name,
#             country=billing_country,
#             street_address=billing_street_address,
#             city=billing_city,
#             phone=billing_phone,
#             zip_code=billing_zip_code,
#             email=billing_email,
#             default=billing_default
#         )
#
#         CustomerAddress.objects.create(
#             order=order_instance,
#             address_type='Shipping',
#             first_name=shipping_first_name,
#             last_name=shipping_last_name,
#             country=shipping_country,
#             street_address=shipping_street_address,
#             city=shipping_city,
#             phone=shipping_phone,
#             zip_code=shipping_zip_code,
#             email=shipping_email,
#         )
#
#         # work with coupon start
#         coupon_status = validated_data.pop('coupon_status')
#
#         if coupon_status == True:
#             coupon = validated_data.pop('coupon')
#             coupon_id = Coupon.objects.get(id=coupon.id)
#             user_id = User.objects.get(id=self.context['request'].user.id)
#             coupon_obj = Coupon.objects.filter(id=coupon.id)
#             check_in_use_coupon_record = UseRecordOfCoupon.objects.filter(
#                 coupon_id=coupon_obj[0].id, user_id=self.context['request'].user.id).exists()
#             if check_in_use_coupon_record:
#                 pass
#             else:
#                 UseRecordOfCoupon.objects.create(
#                     coupon_id=coupon_id, user_id=user_id)
#                 number_of_uses = int(coupon_obj[0].number_of_uses)
#                 coupon_obj.update(number_of_uses=number_of_uses - 1)
#                 number_of_uses = Coupon.objects.get(
#                     code=coupon_obj[0].code).number_of_uses
#                 if number_of_uses < 1:
#                     coupon_obj.update(is_active=False)
#         # work with coupon end
#
#         return order_instance

class ProductItemCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id',
                  'product',
                  'quantity',
                  'unit_price'
                  ]

class CheckoutSerializer(serializers.ModelSerializer):
    order_items = ProductItemCheckoutSerializer(many=True, required=False)
    coupon_status = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'product_count', 'total_price', 'coupon', 'coupon_status',
                  'coupon_discount_amount', 'tax_amount', 'payment_type', 'shipping_cost', 'order_items', 'delivery_address', 'comment']

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        payment_type = validated_data.get('payment_type')
        order_status = "PENDING"
        payment_status = "UN-PAID"

        if payment_type:
            type_name_org = PaymentType.objects.get(id=payment_type.id).type_name
            type_name = type_name_org.lower()
            if type_name != 'cash on delivery':
                order_status = "CONFIRMED"
                payment_status = "PAID"

        order_instance = Order.objects.create(
            **validated_data, user=self.context['request'].user, order_status=order_status,
            payment_status=payment_status )

        if order_items:
            count = 0

            for order_item in order_items:
                product = order_item['product']
                quantity = order_item['quantity']
                unit_price = order_item['unit_price']
                total_price = float(unit_price) * float(quantity)
                order_item_instance = OrderItem.objects.create(order=order_instance, product=product, quantity=int(
                    quantity), unit_price=unit_price)

                product_obj = Product.objects.get(id=product.id)

                # update inventory
                if payment_status == 'PAID':
                    product_filter_obj = Product.objects.filter(id=product.id)
                    inventory_obj = Inventory.objects.filter(product=product).latest('created_at')
                    new_update_quantity = int(inventory_obj.current_quantity) - int(quantity)
                    product_filter_obj.update(quantity = new_update_quantity)
                    inventory_obj.current_quantity = new_update_quantity
                    inventory_obj.save()

                # product sell count update
                count += 1
                product_sell_quan = Product.objects.filter(
                    slug=product_obj.slug)[0].sell_count
                product_sell_quan += 1
                Product.objects.filter(slug=product_obj.slug).update(
                    sell_count=product_sell_quan)

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
                coupon_obj.update(number_of_uses=number_of_uses - 1, is_active=True)
                number_of_uses = Coupon.objects.get(
                    code=coupon_obj[0].code).number_of_uses
                if number_of_uses < 1:
                    coupon_obj.update(is_active=False)
        # work with coupon end

        return order_instance
