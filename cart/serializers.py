from rest_framework import serializers
from .models import *
from product.models import Product, Inventory, Specification
from product.serializers import SpecificationSerializer


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


class PaymentTypesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = [
            'id',
            'type_name',
            'note'
        ]


class ApplyCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'amount']


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


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'subtotal']


class ProductItemCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id',
                  'product',
                  'quantity',
                  'unit_price',
                  'warranty'
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

                try:
                    warranty = order_item['warranty']
                except:
                    warranty = ''


                order_item_instance = OrderItem.objects.create(order=order_instance, product=product, quantity=int(
                    quantity), unit_price=unit_price, total_price=total_price, warranty=warranty)

                product_obj = Product.objects.get(id=product.id)

                # update inventory
                if order_instance.payment_status == 'PAID':
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
