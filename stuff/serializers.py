from rest_framework import serializers
from stuff.models import Role
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


class UpdateStuffSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'email': {'required': True},
                        'password': {'write_only': True, 'required': False}
                        }
        model = User
        fields = ['id', 'name', 'email', 'phone', 'password', 'role']


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'title']