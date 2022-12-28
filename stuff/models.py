from django.db import models
from ecommerce.models import AbstractTimeStamp
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class Role(AbstractTimeStamp):
    title = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        db_table = 'role'

    def __str__(self):
        return self.title


class PermissionModules(AbstractTimeStamp):
    title = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'PermissionModule'
        verbose_name_plural = 'PermissionModules'
        db_table = 'permission_modules'

    def __str__(self):
        return self.title


class RolePermissions(AbstractTimeStamp):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions_role', blank=True, null=True)
    permission_module = models.ForeignKey(PermissionModules, on_delete=models.CASCADE, related_name='role_permissions_permission_module', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'RolePermission'
        verbose_name_plural = 'RolePermissions'
        db_table = 'role_permission'

    def __str__(self):
        return 'Role: ' + self.role.title + ' Permission: ' + self.permission_module.title

