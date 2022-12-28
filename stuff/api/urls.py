from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from stuff.api.views import StuffListAPI, CreateStuffAPI

urlpatterns = [
    path('stuff/stuff-list/<int:pagination>/', StuffListAPI.as_view(), name='stuff_list'),
    path('stuff/create-stuff/', CreateStuffAPI.as_view(), name='create_stuff'),
]