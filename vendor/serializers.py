from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ecommerce.common.emails import send_email_without_delay
from product.models import Brand, Category, SubCategory, SubSubCategory, Units
from user.models import User
from user.serializers import UserRegisterSerializer
from vendor.models import VendorRequest, Vendor, StoreSettings


class VendorRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorRequest
        fields = ['id', 'first_name', 'last_name', 'organization_name',
                  'email', 'vendor_type', 'nid', 'trade_license']
        # fields = ['id', 'email', 'organization_name', 'first_name', 'last_name', 'vendor_type', 'nid', 'trade_license']


class VendorCreateSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField(write_only=True)
    request_id = serializers.IntegerField(write_only=True)
    vendor_request = VendorRequestSerializer(read_only=True)
    vendor_admin = UserRegisterSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'organization_name', 'address', 'vendor_admin',
                  'vendor_request', 'phone', 'is_verified', 'request_id']
        read_only_fields = ('organization_name', 'address',
                            'vendor_admin', 'vendor_request', 'phone')

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
            if vendor_instance:
                email_list = user.email
                subject = "Your Account"
                html_message = render_to_string('vendor_email.html',
                                                {'username': user.first_name, 'email': user.email, 'password': password})
                send_email_without_delay(subject, html_message, email_list)
            return vendor_instance
        else:
            raise ValidationError("You should verify first to create a vendor")


class OrganizationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRequest
        fields = ['organization_name']


class VendorDetailSerializer(serializers.ModelSerializer):
    vendor_request = VendorRequestSerializer(read_only=True)
    vendor_admin = UserRegisterSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'organization_name', 'vendor_admin',
                  'vendor_request', 'address', 'phone']


class StoreSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreSettings
        fields = ['id', 'store_name', 'address', 'email', 'phone', 'logo',
                  'banner', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin']

    def create(self, validated_data):
        user = self.context['request'].user
        vendor = Vendor.objects.get(vendor_admin=user)
        store_settings_instance = StoreSettings.objects.create(
            **validated_data, vendor=vendor)
        return store_settings_instance


class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "vendor category serializer"
        model = Category
        fields = ['id', 'title']


class VendorSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title']


class VendorSubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title']


class VendorBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


class VendorUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'title']
