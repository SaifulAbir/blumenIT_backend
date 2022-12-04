from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from user import models as user_models
from user.models import CustomerProfile, Subscription, User, OTPModel


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