
from rest_framework.generics import ListAPIView
from currency.models import Currency
from currency.serializers import CurrencyListSerializer
from rest_framework.permissions import AllowAny
class CurrencyListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Currency.objects.all().order_by('-created_at')
    serializer_class = CurrencyListSerializer