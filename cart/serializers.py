from rest_framework import serializers
from .models import *
from product.models import Product, Inventory, Specification, ShippingClass
from product.serializers import SpecificationSerializer
from rest_framework.exceptions import ValidationError
import datetime





class ProductSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'thumbnail', 'title', 'price', 'total_quantity']

    def get_total_quantity(self, obj):
        quantity = Product.objects.get(id=obj.id).quantity
        return quantity


class CheckoutDetailsOrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title',read_only=True)
    product_sku = serializers.CharField(source='product.sku',read_only=True)
    product_thumb = serializers.ImageField(source='product.thumbnail',read_only=True)
    product_price = serializers.SerializerMethodField()
    product_specification = serializers.SerializerMethodField('get_product_specification')
    product_warranty_title = serializers.CharField(source='product_warranty.warranty.title',read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_title', 'product_thumb', 'product_price', 'product_sku', 'product_specification', 'quantity', 'unit_price', 'unit_price_after_add_warranty', 'total_price', 'product_warranty', 'product_warranty_title']

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
    delivery_date = serializers.SerializerMethodField('get_delivery_date')
    vat_amount =  serializers.FloatField(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'user_phone', 'order_id', 'order_date', 'delivery_date', 'order_status', 'order_items', 'delivery_address', 'payment_type', 'payment_title', 'product_price', 'coupon_discount_amount', 'sub_total', 'shipping_class', 'shipping_cost', 'total_price', 'vat_amount']

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
            if order_item.unit_price_after_add_warranty != 0.0:
                price = order_item.unit_price_after_add_warranty
            quantity = order_item.quantity
            t_price = float(price) * float(quantity)
            prices.append(t_price)
        if obj.vat_amount:
            sub_total = float(sum(prices)) + float(obj.vat_amount)
        else:
            sub_total = float(sum(prices))
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
        total_price = 0.0
        for order_item in order_items:
            price = order_item.unit_price
            if order_item.unit_price_after_add_warranty != 0.0:
                price = order_item.unit_price_after_add_warranty
            quantity = order_item.quantity
            t_price = float(price) * float(quantity)
            prices.append(t_price)
        if obj.vat_amount:
            sub_total = float(sum(prices)) + float(obj.vat_amount)
        else:
            sub_total = float(sum(prices))
        if sub_total:
            total_price += sub_total

        shipping_cost = obj.shipping_cost
        if shipping_cost:
            total_price += shipping_cost

        coupon_discount_amount = obj.coupon_discount_amount
        if coupon_discount_amount:
            total_price -= coupon_discount_amount
        return total_price

    def get_delivery_date(self, obj):
        try:
            if obj.shipping_class:
                delivery_days = ShippingClass.objects.get(id=obj.shipping_class.id).delivery_days
                order_date = obj.order_date
                order_date_c = datetime.datetime.strptime(str(order_date), "%Y-%m-%d")
                delivery_date = order_date_c + datetime.timedelta(days=int(delivery_days))
                return delivery_date.date()
            else:
                return ''
        except:
            return ''

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
        fields = ['id', 'code', 'min_shopping_amount', 'amount', 'quantity', 'number_of_uses', 'start_time', 'is_active']


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['id', 'user', 'name', 'address', 'phone',
                  'email', 'zip_code', 'country', 'city', 'state', 'shipping_cost', 'shipping_class']

    def create(self, validated_data):
        address_instance = DeliveryAddress.objects.create(**validated_data, user=self.context['request'].user)
        return address_instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_id', 'product_count', 'order_date', 'order_status', 'total_price']


class OrderItemSerializer(serializers.ModelSerializer):
    # order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        # fields = ['id', 'order', 'product', 'quantity', 'subtotal']
        fields = ['id', 'product', 'quantity', 'unit_price', 'unit_price_after_add_warranty', 'subtotal']


class ProductItemCheckoutSerializer(serializers.ModelSerializer):
    product_warranty = serializers.PrimaryKeyRelatedField(queryset=ProductWarranty.objects.all(), many=False, write_only=True, required= False)
    class Meta:
        model = OrderItem
        fields = ['id',
                  'product',
                  'quantity',
                  'unit_price',
                  'product_warranty',
                  ]


class CheckoutSerializer(serializers.ModelSerializer):
    order_items = ProductItemCheckoutSerializer(many=True, required=False)
    coupon_status = serializers.BooleanField(write_only=True, required=False)
    order_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'product_count', 'coupon', 'coupon_status', 'coupon_discount_amount', 'payment_type', 'shipping_class', 'shipping_cost', 'order_items', 'delivery_address', 'comment']

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

        # stop take order process if any product out of stock
        if order_items:
            for order_item in order_items:
                product = order_item['product']
                quantity = order_item['quantity']
                inventory_obj = Inventory.objects.filter(product=product).latest('created_at')
                new_update_quantity = int(inventory_obj.current_quantity) - int(quantity)
                if int(new_update_quantity) < 0:
                    raise ValidationError("Order didn't create. One of product out of stock.")

        # stop take order process if order items have in_house and also normal products
        # if order_items:
        #     order_items_in_house_product = 0
        #     order_items_not_in_house_product = 0
        #     for order_item in order_items:
        #         product = order_item['product']
        #         if product.in_house_product == True:
        #             order_items_in_house_product += 1
        #         if product.in_house_product == False:
        #             order_items_not_in_house_product += 1

        #     total_order_items = int(len(order_items))
        #     in_house_order = True
        #     if order_items_in_house_product == total_order_items:
        #         in_house_order = True
        #         pass
        #     elif order_items_not_in_house_product == total_order_items:
        #         in_house_order = False
        #         pass
        #     else:
        #         raise ValidationError("Order didn't create, Because of multiple products types available in order items.")


        order_instance = Order.objects.create(
            **validated_data, user=self.context['request'].user, order_status=order_status,
            payment_status=payment_status)

        if order_items:
            count = 0
            vat_amount_list = []
            for order_item in order_items:
                product = order_item['product']
                quantity = order_item['quantity']
                unit_price = order_item['unit_price']

                total_price = float(unit_price) * float(quantity)

                try:
                    product_warranty = order_item['product_warranty']
                except:
                    product_warranty = None

                if product_warranty:
                    warranty_value = product_warranty.warranty_value
                    warranty_value_type = product_warranty.warranty_value_type

                    if warranty_value_type == 'PERCENTAGE':
                        unit_price_after_add_warranty = float((float(unit_price) / 100) * float(warranty_value))
                        unit_price_after_add_warranty = unit_price + unit_price_after_add_warranty
                    elif warranty_value_type == 'FIX':
                        unit_price_after_add_warranty = float(float(unit_price) + float(warranty_value))
                        unit_price_after_add_warranty = unit_price + unit_price_after_add_warranty

                    total_price =  float(unit_price_after_add_warranty) * float(quantity)

                    OrderItem.objects.create(order=order_instance, product=product, quantity=int(quantity), unit_price=unit_price, total_price=total_price, product_warranty=product_warranty, unit_price_after_add_warranty=unit_price_after_add_warranty)
                else:
                    OrderItem.objects.create(order=order_instance, product=product, quantity=int(quantity), unit_price=unit_price, total_price=total_price)

                # update inventory
                inventory_obj = Inventory.objects.filter(product=product).latest('created_at')
                new_update_quantity = int(inventory_obj.current_quantity) - int(quantity)
                Product.objects.filter(id=product.id).update(quantity = new_update_quantity)
                inventory_obj.current_quantity = new_update_quantity
                inventory_obj.save()

                # product sell count update
                count += 1
                product_sell_quan = Product.objects.filter(
                    slug=product.slug)[0].sell_count
                product_sell_quan += 1
                Product.objects.filter(slug=product.slug).update(
                    sell_count=product_sell_quan)

                # vat calculation in percent logic
                product_vat_value = Product.objects.filter(slug=product.slug)[0].vat
                if product_vat_value:
                    vat_amount = float((float(total_price) / 100) * float(product_vat_value))
                    vat_amount_list.append(vat_amount)

                print("vat_amount_list")
                print(vat_amount_list)


            Order.objects.filter(id=order_instance.id).update(vat_amount = sum(vat_amount_list))


        # work with coupon start
        try:
            coupon_status = validated_data.pop('coupon_status')
        except:
            coupon_status = None

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
                UseRecordOfCoupon.objects.create(coupon_id=coupon_id, user_id=user_id)
                quantity = int(coupon_obj[0].quantity)
                number_of_uses = int(coupon_obj[0].number_of_uses)
                coupon_obj.update(number_of_uses=number_of_uses + 1, is_active=True)
                number_of_uses_after_update = Coupon.objects.get(
                    code=coupon_obj[0].code).number_of_uses
                if quantity < number_of_uses_after_update :
                    coupon_obj.update(is_active=False)
        # work with coupon end

        return order_instance


class ShippingClassDataSerializer(serializers.ModelSerializer):
    shipping_country_name = serializers.CharField(source='shipping_country.title',read_only=True)
    shipping_state_name = serializers.CharField(source='shipping_state.title',read_only=True)
    shipping_city_name = serializers.CharField(source='shipping_city.title',read_only=True)
    state_city_concate = serializers.SerializerMethodField('get_state_city_concate')
    class Meta:
        model = ShippingClass
        fields = ['id', 'description', 'shipping_country', 'shipping_country_name', 'shipping_state', 'shipping_state_name', 'shipping_city', 'shipping_city_name', 'delivery_days', 'delivery_charge', 'state_city_concate']

    def get_state_city_concate(self, obj):
        c_name = obj.shipping_state.title + ' ' + obj.shipping_city.title
        return c_name
