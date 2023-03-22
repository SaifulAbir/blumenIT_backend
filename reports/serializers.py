from rest_framework import serializers
from cart.models import Order, OrderItem, Wishlist
from product.models import Product, Inventory
from vendor.models import Seller, StoreSettings
from django.db.models import Q

class SalesReportSerializer(serializers.ModelSerializer):
    num_of_product = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source="user.name", read_only=True)
    customer_email = serializers.CharField(source="user.email", read_only=True)
    customer_phone = serializers.CharField(source="user.phone", read_only=True)
    # total_price = serializers.SerializerMethodField('get_total_price')
    vat_amount = serializers.FloatField(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'num_of_product', 'customer_name', 'customer_email', 'customer_phone', 'total_price', 'order_status', 'payment_status', 'refund', 'order_date', 'vat_amount', 'discount_amount']

    def get_num_of_product(self, obj):
        try:
            number = OrderItem.objects.filter(order=obj).count()
            return number
        except:
            return 0

    # def get_total_price(self, obj):
    #     order_items = OrderItem.objects.filter(order=obj)
    #     prices = []
    #     total_price = 0.0
    #     for order_item in order_items:
    #         price = order_item.unit_price
    #         if order_item.unit_price_after_add_warranty != 0.0:
    #             price = order_item.unit_price_after_add_warranty
    #         quantity = order_item.quantity
    #         t_price = float(price) * float(quantity)
    #         prices.append(t_price)
    #     if obj.vat_amount:
    #         sub_total = float(sum(prices)) + float(obj.vat_amount)
    #     else:
    #         sub_total = float(sum(prices))
    #     if sub_total:
    #         total_price += sub_total

    #     shipping_cost = obj.shipping_cost
    #     if shipping_cost:
    #         total_price += shipping_cost

    #     coupon_discount_amount = obj.coupon_discount_amount
    #     if coupon_discount_amount:
    #         total_price -= coupon_discount_amount

    #     discount_amount = obj.discount_amount
    #     if discount_amount:
    #         total_price -= discount_amount

    #     return total_price


class VendorProductReportSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source="order.order_id", read_only=True)
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_price = serializers.CharField(source="product.price", read_only=True)
    order_date = serializers.CharField(source="order.order_date", read_only=True)
    order_status = serializers.CharField(source="order.order_status", read_only=True)
    seller_name = serializers.SerializerMethodField('get_seller_name')
    product_vat = serializers.CharField(source='product.vat',read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product_title', 'product_price', 'quantity', 'order_date', 'order_status', 'seller_name', 'product_vat']

    def get_seller_name(self, obj):
        seller_name = obj.product.seller.name
        return seller_name


class InHouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'sell_count', 'category']


class SellerProductSaleSerializer(serializers.ModelSerializer):
    shop_name =  serializers.SerializerMethodField()
    number_of_product_sale =  serializers.SerializerMethodField()
    order_amount =  serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = ['id', 'name', 'shop_name', 'number_of_product_sale', 'order_amount', 'status']

    def get_shop_name(self, obj):
        store_name_obj = StoreSettings.objects.filter(Q(seller = obj.id )).exists()
        if store_name_obj:
            store_name_ob = StoreSettings.objects.get(seller = obj.id)
            store_name = store_name_ob.store_name
        else:
            store_name = ''
        return store_name

    def get_number_of_product_sale(self, obj):
        order_item_obj = OrderItem.objects.filter(Q(product__seller = obj.id)).exists()
        if order_item_obj:
            order_item_ob = OrderItem.objects.filter(Q(product__seller = obj.id)).count()
        else:
            order_item_ob = 0

        return order_item_ob

    def get_order_amount(self, obj):
        order_item_obj = OrderItem.objects.filter(Q(product__seller = obj.id)).exists()
        order_amount = 0
        if order_item_obj:
            order_item_ob_l = OrderItem.objects.filter(Q(product__seller = obj.id))
            for i in order_item_ob_l:
                order_amount += float(i.quantity * i.unit_price)
        else:
            order_amount = 0

        return order_amount


class ProductStockSerializer(serializers.ModelSerializer):
    stock =  serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'short_description', 'stock', 'category']

    def get_stock(self, obj):
        inventory_obj = Inventory.objects.filter(Q(product = obj.id)).exists()
        if inventory_obj:
            inventory_obj_l = Inventory.objects.filter(Q(product = obj.id)).latest('created_at')
            stock_count = inventory_obj_l.current_quantity
        else:
            stock_count = 0

        return stock_count


class ProductWishlistSerializer(serializers.ModelSerializer):
    count =  serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'count', 'category']

    def get_count(self, obj):
        wishlist_obj = Wishlist.objects.filter(Q(product = obj.id)).exists()
        if wishlist_obj:
            wishlist_count = Wishlist.objects.filter(Q(product = obj.id)).count()
        else:
            wishlist_count = 0

        return wishlist_count