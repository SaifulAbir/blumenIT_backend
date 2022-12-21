from rest_framework import serializers
from cart.models import Order

class SalesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_id']