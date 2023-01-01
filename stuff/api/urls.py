from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from stuff.api.views import StuffListAPI, CreateStuffAPI, UpdateStuffAPIView, RoleListAPIView

urlpatterns = [
    path('stuff/stuff-list/<int:pagination>/', StuffListAPI.as_view(), name='stuff_list'),
    path('stuff/create-stuff/', CreateStuffAPI.as_view(), name='create_stuff'),
    path('stuff/update-stuff/<int:id>/', UpdateStuffAPIView.as_view(), name='update_stuff'),
    path('stuff/role-list/<int:pagination>/', RoleListAPIView.as_view(), name='role_list'),
    # path('stuff/create-role/<int:pagination>/', CreatreRoleAPIView.as_view(), name='create_role'),
]