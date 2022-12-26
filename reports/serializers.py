from rest_framework import serializers
from cart.models import Order, OrderItem

class SalesReportSerializer(serializers.ModelSerializer):
    num_of_product = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source="user.name", read_only=True)
    customer_email = serializers.CharField(source="user.email", read_only=True)
    customer_phone = serializers.CharField(source="user.phone", read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'num_of_product', 'customer_name', 'customer_email', 'customer_phone', 'total_price', 'delivery_status', 'payment_status', 'refund']

    def get_num_of_product(self, obj):
        try:
            number = OrderItem.objects.filter(order=obj).count()
            return number
        except:
            return 0