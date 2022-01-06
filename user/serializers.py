from rest_framework import serializers
from user import models as user_models


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