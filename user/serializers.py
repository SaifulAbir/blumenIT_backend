from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from user import models as user_models
from user.models import CustomerProfile, Subscription, User, OTPModel
from cart.models import Order, OrderItem, DeliveryAddress
from product.models import Product, SavePc, SavePcItems, SubCategory, ShippingClass
from cart.models import Wishlist
from product.serializers import ProductListBySerializer
import datetime


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
    total_price = serializers.SerializerMethodField('get_total_price')
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_id', 'order_date', 'order_status', 'vat_amount', 'total_price']

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


class CustomerOrderItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_thumb = serializers.ImageField(source='product.thumbnail',read_only=True)
    product_price = serializers.SerializerMethodField()
    product_slug = serializers.CharField(source='product.slug',read_only=True)
    product_warranty_title = serializers.CharField(source='product_warranty.warranty.title',read_only=True)
    unit_price = serializers.SerializerMethodField('get_unit_price')
    product_vat = serializers.CharField(source='product.vat',read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_thumb', 'product_slug', 'product_price', 'quantity', 'unit_price', 'total_price', 'product_warranty', 'product_warranty_title', 'product_vat']

    def get_product_name(self, obj):
        product_name = Product.objects.filter(id=obj.product.id)[0].title
        return product_name

    def get_product_price(self, obj):
        product_price = Product.objects.filter(id=obj.product.id)[0].price
        return product_price

    def get_unit_price(self, obj):
        unit_price = obj.unit_price
        if obj.unit_price_after_add_warranty != 0.0:
            unit_price = obj.unit_price_after_add_warranty
        return unit_price


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
    delivery_date = serializers.SerializerMethodField('get_delivery_date')
    vat_amount =  serializers.FloatField(read_only=True)
    class Meta:
        model = Order
        fields = ['user', 'order_id', 'order_date', 'delivery_date', 'order_status', 'order_items', 'delivery_address', 'payment_type', 'payment_title', 'sub_total', 'shipping_cost', 'coupon_discount_amount', 'total_price', 'vat_amount']

    def get_order_items(self, obj):
        queryset = OrderItem.objects.filter(order=obj)
        serializer = CustomerOrderItemsSerializer(instance=queryset, many=True, context={'request': self.context['request']})
        return serializer.data

    def get_delivery_address(self, obj):
        try:
            queryset = DeliveryAddress.objects.filter(id=obj.delivery_address.id)
            serializer = CustomerDeliveryAddressSerializer(instance=queryset, many=True)
            return serializer.data
        except:
            return None

    def get_sub_total(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        prices = []
        for order_item in order_items:
            price = order_item.unit_price
            quantity = order_item.quantity
            t_price = float(price) * float(quantity)
            prices.append(t_price)
        if obj.vat_amount:
            sub_total = float(sum(prices)) + float(obj.vat_amount)
        else:
            sub_total = float(sum(prices))
        return sub_total

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

class CustomerProfileOtherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'birth_date',
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    avatar = serializers.SerializerMethodField(read_only=True)
    birth_date = serializers.SerializerMethodField(read_only=True)
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
                    CustomerProfile.objects.create(user=instance, birth_date=birth_date)
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


class WishlistDataSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField('get_product')
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product_data']

    def get_product(self, obj):
        queryset = Product.objects.filter(id=obj.product.id)
        serializer = ProductListBySerializer(instance=queryset, many=True)
        return serializer.data


class SavePcItemsSerializer(serializers.ModelSerializer):
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.filter(pc_builder=True), many=False, write_only=True, required= True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(status='PUBLISH'), many=False, write_only=True, required= False)
    class Meta:
        model = SavePcItems
        fields = [
            'id',
            'sub_category',
            'product'
        ]

class SavePcCreateSerializer(serializers.ModelSerializer):
    save_pc_items = SavePcItemsSerializer(many=True, required=False)
    class Meta:
        model = SavePc
        fields = ['id', 'title', 'description', 'save_pc_items']

    def create(self, validated_data):
         # save_pc_items
        try:
            save_pc_items = validated_data.pop('save_pc_items')
        except:
            save_pc_items = ''

        save_pc_instance = SavePc.objects.create(**validated_data, user=self.context['request'].user )

        try:
            # save_pc_items
            if save_pc_items:
                for save_pc_item in save_pc_items:
                    sub_category = save_pc_item['sub_category']
                    product = save_pc_item['product']
                    save_pc_items_instance = SavePcItems.objects.create(save_pc=save_pc_instance, sub_category=sub_category, product=product)

            return save_pc_instance
        except:
            return save_pc_instance


class SavaPcDataSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")
    class Meta:
        model = SavePc
        fields = ['id', 'title', 'description', 'created_at']


class SavePcItemsProductDetailsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    qty = serializers.IntegerField(default=1)
    price = serializers.SerializerMethodField('get_price')
    imgUrl = serializers.ImageField(source="thumbnail",read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'qty', 'price', 'imgUrl']

    def get_name(self, obj):
        return obj.title

    def get_price(self, obj):
        return obj.price


class SavePcItemsDetailsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="sub_category.title",read_only=True)
    icon = serializers.ImageField(source="sub_category.icon",read_only=True)
    type = serializers.CharField(default='sub_category')
    item = serializers.SerializerMethodField('get_item')
    class Meta:
        model = SavePcItems
        fields = ['id', 'title', 'icon', 'type', 'item']

    def get_item(self, obj):
        selected_item = Product.objects.filter(id=obj.product.id)
        return SavePcItemsProductDetailsSerializer(selected_item, many=True, context={'request': self.context['request']}).data


class SavePcDetailsSerializer(serializers.ModelSerializer):
    save_pc_items = serializers.SerializerMethodField('get_save_pc_items')
    class Meta:
        model = SavePc
        fields = ['id', 'title', 'save_pc_items']

    def get_save_pc_items(self, obj):
        selected_save_pc_items = SavePcItems.objects.filter(save_pc=obj, is_active=True)
        return SavePcItemsDetailsSerializer(selected_save_pc_items, many=True, context={'request': self.context['request']}).data


class AccountDeleteRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name','delete_request', 'is_active']


class AccountDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name','delete_request', 'is_active']


