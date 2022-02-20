from rest_framework import serializers
from user import models as user_models
from user.models import CustomerProfile, Subscription


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}}
        fields = ('first_name', 'last_name', 'email', 'password')
        model = user_models.User

    def create(self, validated_data):
        user = user_models.User.objects.create_user(
            **validated_data, username=validated_data['email'], is_active=False)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login endpoint.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(read_only=True)
    gender_display_value = serializers.CharField(
        source='get_gender_display', read_only=True
    )
    class Meta:
        model = CustomerProfile
        model_fields = ['id', 'user', 'phone', 'address', 'birth_date', 'gender', 'gender_display_value']
        fields = model_fields


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        model_fields = ['email',]
        fields = model_fields