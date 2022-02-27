from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from user.models import User
from user.serializers import UserRegisterSerializer
from vendor.models import VendorRequest, Vendor


class VendorRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorRequest
        fields = ['id', 'email', 'organization_name', 'first_name', 'last_name', 'vendor_status', 'nid', 'trade_license']


class VendorCreateSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField(write_only=True)
    request_id = serializers.IntegerField(write_only=True)
    vendor_request = VendorRequestSerializer(read_only=True)
    vendor_admin = UserRegisterSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'organization_name', 'address', 'vendor_admin', 'vendor_request', 'phone', 'is_verified', 'request_id']
        read_only_fields = ('organization_name', 'address', 'vendor_admin', 'vendor_request', 'phone')

    def create(self, validated_data):
        is_verified = validated_data.pop('is_verified')
        request_id = validated_data.pop('request_id')
        if is_verified is True:
            password = User.objects.make_random_password()
            vendor_request = VendorRequest.objects.get(id=request_id)
            vendor_request.is_verified = True
            vendor_request.save()

            user = User.objects.create(username=vendor_request.email, email=vendor_request.email,
                                first_name=vendor_request.first_name, last_name=vendor_request.last_name)
            user.set_password(password)
            user.save()

            vendor_instance = Vendor.objects.create(organization_name=vendor_request.organization_name,
                                                    vendor_admin=user, vendor_request=vendor_request, password=password)
            return vendor_instance
        else:
            raise ValidationError("You should verify first to create a vendor")