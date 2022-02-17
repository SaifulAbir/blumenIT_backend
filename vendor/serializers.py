from rest_framework import serializers
from vendor.models import VendorRequest


class VendorRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorRequest
        fields = ['id', 'email', 'organization_name', 'first_name', 'last_name', 'vendor_status', 'nid', 'trade_license']