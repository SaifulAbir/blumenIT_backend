from rest_framework import serializers
from stuff.models import Role, PermissionModules, RolePermissions
from user.models import User
from django.db.models import Q
from user import models as user_models
from django.utils import timezone

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


class RoleCreateSerializer(serializers.ModelSerializer):
    permission_modules = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=True)
    class Meta:
        model = Role
        fields = ['id', 'title', 'permission_modules']

    def create(self, validated_data):

        # permission_modules
        try:
            permission_modules = validated_data.pop('permission_modules')
        except:
            permission_modules = ''

        role_instance = Role.objects.create(**validated_data)

        try:
            # permission_modules
            if permission_modules:
                for permission_module_id in permission_modules:
                    if PermissionModules.objects.filter(id=permission_module_id).exists():
                        permission_obj = PermissionModules.objects.get(id=permission_module_id)
                        try:
                            RolePermissions.objects.create(role=role_instance, permission_module = permission_obj)
                        except:
                            pass
                    else:
                        pass
            return role_instance
        except:
            return role_instance


class RoleUpdateSerializer(serializers.ModelSerializer):
    existing_permission_modules = serializers.SerializerMethodField()
    permission_modules = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Role
        fields = ['id', 'title', 'existing_permission_modules', 'permission_modules']

    def get_existing_permission_modules(self, obj):
        permission_modules_list = []
        try:
            selected_permission_modules = RolePermissions.objects.filter(role=obj, is_active=True)
            for s_p_m in selected_permission_modules:
                permission_module_id = s_p_m.permission_module.id
                permission_modules_list.append(permission_module_id)
            return permission_modules_list
        except:
            return permission_modules_list

    def update(self, instance, validated_data):
        # permission_modules
        try:
            permission_modules = validated_data.pop('permission_modules')
        except:
            permission_modules = ''

        try:
            # permission_modules
            if permission_modules:
                RolePermissions.objects.filter(role=instance).delete()
                for permission_module_id in permission_modules:
                    if PermissionModules.objects.filter(id=permission_module_id).exists():
                        permission_obj = PermissionModules.objects.get(id=permission_module_id)
                        try:
                            RolePermissions.objects.create(role=instance, permission_module = permission_obj)
                        except:
                            pass
                    else:
                        pass
            else:
                RolePermissions.objects.filter(role=instance).delete()

            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)

        except:
            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionModules
        fields = ['id', 'title']