from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from user import models as user_models
from user.models import CustomerProfile, Subscription, User, OTPModel
from cart.models import Order, OrderItem, DeliveryAddress
from product.models import Product


class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True},
                        'phone': {'required': True}}
        fields = ('phone', 'email', 'password')
        model = user_models.User


class OTPSendSerializer(serializers.ModelSerializer):
    is_login = serializers.BooleanField(required=True, write_only=True)
    class Meta:
        extra_kwargs = {'email': {'required': True},
                        'phone': {'required': True}}
        fields = ('email', 'phone', 'is_login')
        model = user_models.User


class OTPReSendSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'contact_number': {'required': True}}
        fields = ('contact_number',)
        model = OTPModel


class OTPVerifySerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'contact_number': {'required': True},
                        'otp_number': {'required': True}}
        fields = ('contact_number', 'otp_number')
        model = OTPModel


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login endpoint.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class SuperAdminLoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        model_fields = ['email',]
        fields = model_fields


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class CustomerOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_id', 'order_date', 'order_status', 'total_price']


class CustomerOrderItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_thumb = serializers.ImageField(source='product.thumbnail',read_only=True)
    product_price = serializers.SerializerMethodField()
    product_slug = serializers.CharField(source='product.slug',read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_thumb', 'product_slug', 'quantity', 'product_price']

    def get_product_name(self, obj):
        product_name = Product.objects.filter(id=obj.product.id)[
            0].title
        return product_name

    def get_product_price(self, obj):
        product_price = Product.objects.filter(id=obj.product.id)[
            0].price
        return product_price


class CustomerDeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['id', 'user', 'name', 'address', 'phone',
                  'email', 'zip_code', 'country', 'city', 'state']


class CustomerOrderDetailsSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField('get_order_items')
    sub_total = serializers.SerializerMethodField('get_sub_total')
    delivery_address = serializers.SerializerMethodField('get_delivery_address')
    payment_title = serializers.CharField(source='payment_type.type_name',read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')
    class Meta:
        model = Order
        fields = ['user', 'order_id', 'order_date', 'delivery_date', 'order_status', 'order_items', 'delivery_address', 'payment_type', 'payment_title', 'sub_total', 'shipping_cost', 'coupon_discount_amount', 'total_price']

    def get_order_items(self, obj):
        queryset = OrderItem.objects.filter(order=obj)
        serializer = CustomerOrderItemsSerializer(instance=queryset, many=True, context={'request': self.context['request']})
        return serializer.data

    def get_delivery_address(self, obj):
        queryset = DeliveryAddress.objects.filter(id=obj.delivery_address.id)
        serializer = CustomerDeliveryAddressSerializer(instance=queryset, many=True)
        return serializer.data

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


class CustomerProfileOtherDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'birth_date',
            'avatar'
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    avatar = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    others_info = CustomerProfileOtherDataSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'phone', 'avatar', 'birth_date', 'others_info']

    def get_avatar(self, obj):
        try:
            get_avatar=CustomerProfile.objects.get(user= obj.id)
            return get_avatar.avatar.url
        except:
            return ''

    def get_birth_date(self, obj):
        try:
            get_birth_date=CustomerProfile.objects.get(user= obj.id)
            return get_birth_date.birth_date
        except:
            return ''

    def update(self, instance, validated_data):

        # flash_deal
        try:
            others_info = validated_data.pop('others_info')
        except:
            others_info = ''

        try:
            if others_info:
                c_p = CustomerProfile.objects.filter(
                    user=instance).exists()
                if c_p == True:
                    CustomerProfile.objects.filter(
                        user=instance).delete()

                for others_in in others_info:
                    birth_date = others_in['birth_date']
                    avatar = others_in['avatar']
                    others_in_instance = CustomerProfile.objects.create(user=instance, birth_date=birth_date, avatar=avatar)
            else:
                c_p = CustomerProfile.objects.filter(
                    user=instance).exists()
                if c_p == True:
                    CustomerProfile.objects.filter(
                        user=instance).delete()

            return super().update(instance, validated_data)
        except:
            return super().update(instance, validated_data)


class CustomerAddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['id', 'name', 'address', 'phone']


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['id', 'name', 'address', 'phone', 'email', 'country', 'city', 'state', 'zip_code', 'default', 'is_active']

    def create(self, validated_data):
        delivery_address_instance = DeliveryAddress.objects.create(**validated_data, user=self.context['request'].user)
        return delivery_address_instance


# class CustomerAddressUpdateSerializer(serializers.ModelSerializer):











# class CustomerProfileSerializer(serializers.ModelSerializer):
#     user = UserRegisterSerializer(read_only=True)
#     gender_display_value = serializers.CharField(
#         source='get_gender_display', read_only=True
#     )
#
#     class Meta:
#         model = CustomerProfile
#         model_fields = ['id', 'user', 'phone', 'address', 'birth_date', 'gender', 'gender_display_value']
#         fields = model_fields

# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         extra_kwargs = {'password': {'write_only': True},
#                         'first_name': {'required': True},
#                         'last_name': {'required': True}}
#         fields = ('first_name', 'last_name', 'email', 'password')
#         model = user_models.User
#
#     def create(self, validated_data):
#         user = user_models.User.objects.create_user(
#             **validated_data, username=validated_data['email'], is_active=False)
#         return user

# class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(write_only=True)
#     last_name = serializers.CharField(write_only=True)
#     user = UserRegisterSerializer(read_only=True)
#     gender_display_value = serializers.CharField(
#         source='get_gender_display', read_only=True
#     )
#     class Meta:
#         model = CustomerProfile
#         model_fields = ['id', 'user', 'phone', 'address', 'birth_date', 'gender', 'gender_display_value',
#                         'first_name', 'last_name']
#         fields = model_fields
#
#     def update(self, instance, validated_data):
#         first_name = validated_data.pop('first_name')
#         last_name = validated_data.pop('last_name')
#         user = User.objects.get(id=instance.user.id)
#         user.first_name=first_name
#         user.last_name=last_name
#         user.save()
#         validated_data.update({"user": user})
#         return super().update(instance, validated_data)