from django.urls import path
from stuff.api.views import StuffListAPI, CreateStuffAPI, UpdateStuffAPIView, RoleListAPIView, AdminRoleCreateAPIView, \
    AdminRoleUpdateAPIView, PermissionListAPIView, AdminPermissionCreateAPIView, AdminPermissionUpdateAPIView

urlpatterns = [
    path('admin/stuff/stuff-list/<int:pagination>/', StuffListAPI.as_view(), name='stuff_list'),
    path('admin/stuff/create-stuff/', CreateStuffAPI.as_view(), name='create_stuff'),
    path('admin/stuff/update-stuff/<int:id>/', UpdateStuffAPIView.as_view(), name='update_stuff'),
    path('admin/stuff/role-list/<int:pagination>/', RoleListAPIView.as_view(), name='role_list'),
    path('admin/stuff/create-role/', AdminRoleCreateAPIView.as_view(), name='create_role'),
    path('admin/stuff/update-role/<int:id>/', AdminRoleUpdateAPIView.as_view(), name='update_role'),

    path('admin/stuff/permission-list/<int:pagination>/', PermissionListAPIView.as_view(), name='permission_list'),
    path('admin/stuff/create-permission/', AdminPermissionCreateAPIView.as_view(), name='create_permission'),
    path('admin/stuff/update-permission/<int:id>/', AdminPermissionUpdateAPIView.as_view(), name='update_permission'),
]