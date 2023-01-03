from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from stuff.api.views import StuffListAPI, CreateStuffAPI, UpdateStuffAPIView, RoleListAPIView, AdminRoleCreateAPIView, \
    AdminRoleUpdateAPIView, PermissionListAPIView, AdminPermissionCreateAPIView, AdminPermissionUpdateAPIView

urlpatterns = [
    path('stuff/stuff-list/<int:pagination>/', StuffListAPI.as_view(), name='stuff_list'),
    path('stuff/create-stuff/', CreateStuffAPI.as_view(), name='create_stuff'),
    path('stuff/update-stuff/<int:id>/', UpdateStuffAPIView.as_view(), name='update_stuff'),
    path('stuff/role-list/<int:pagination>/', RoleListAPIView.as_view(), name='role_list'),
    path('stuff/create-role/', AdminRoleCreateAPIView.as_view(), name='create_role'),
    path('stuff/update-role/<int:id>/', AdminRoleUpdateAPIView.as_view(), name='update_role'),

    path('stuff/permission-list/<int:pagination>/', PermissionListAPIView.as_view(), name='permission_list'),
    path('stuff/create-permission/', AdminPermissionCreateAPIView.as_view(), name='create_permission'),
    path('stuff/update-permission/<int:id>/', AdminPermissionUpdateAPIView.as_view(), name='update_permission'),
]