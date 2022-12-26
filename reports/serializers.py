from rest_framework import serializers
from cart.models import Order, OrderItem
from cart.models import Order

class SalesReportSerializer(serializers.ModelSerializer):
    num_of_product = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source="user.name", read_only=True)
    customer_email = serializers.CharField(source="user.email", read_only=True)
    customer_phone = serializers.CharField(source="user.phone", read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'num_of_product', 'customer_name', 'customer_email', 'customer_phone', 'total_price', 'order_status', 'payment_status', 'refund', 'order_date']

    def get_num_of_product(self, obj):
        try:
            number = OrderItem.objects.filter(order=obj).count()
            return number
        except:
            return 0


class VendorProductReportSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source="order.order_id", read_only=True)
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_price = serializers.CharField(source="product.price", read_only=True)
    order_date = serializers.CharField(source="order.order_date", read_only=True)
    order_status = serializers.CharField(source="order.order_status", read_only=True)
    seller = serializers.CharField(source="order.vendor.name", read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product_title', 'product_price', 'quantity', 'order_date', 'order_status', 'seller']