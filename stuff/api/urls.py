from django.urls import path
from stuff.api.views import StuffListAPI, CreateStuffAPI, UpdateStuffAPIView, RoleListAPIView, AdminRoleCreateAPIView, \
    AdminRoleUpdateAPIView, PermissionListAPIView, AdminPermissionCreateAPIView, AdminPermissionUpdateAPIView, \
    AdminStuffDeleteAPIView

urlpatterns = [
    path('admin/staff/staff-list/<int:pagination>/', StuffListAPI.as_view(), name='stuff_list'),
    path('admin/staff/create-staff/', CreateStuffAPI.as_view(), name='create_stuff'),
    path('admin/staff/update-staff/<int:id>/', UpdateStuffAPIView.as_view(), name='update_stuff'),
    path('admin/staff/staff-delete/<int:id>/', AdminStuffDeleteAPIView.as_view()),
    path('admin/staff/role-list/<int:pagination>/', RoleListAPIView.as_view(), name='role_list'),
    path('admin/staff/create-role/', AdminRoleCreateAPIView.as_view(), name='create_role'),
    path('admin/staff/update-role/<int:id>/', AdminRoleUpdateAPIView.as_view(), name='update_role'),

    path('admin/staff/permission-list/<int:pagination>/', PermissionListAPIView.as_view(), name='permission_list'),
    path('admin/staff/create-permission/', AdminPermissionCreateAPIView.as_view(), name='create_permission'),
    path('admin/staff/update-permission/<int:id>/', AdminPermissionUpdateAPIView.as_view(), name='update_permission'),
]