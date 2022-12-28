from rest_framework import serializers
# from stuff.models import
from user.models import User
from django.db.models import Q
from user import models as user_models

class StuffListSerializer(serializers.ModelSerializer):
    role_title = serializers.CharField(source="role.title", read_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'role_title']


class CreateStuffSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'email': {'required': True},
                        'phone': {'required': True},
                        'password': {'write_only': True}
                        }
        fields = ['name', 'email', 'phone', 'password', 'role']
        model = user_models.User