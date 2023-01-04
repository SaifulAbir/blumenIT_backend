from rest_framework import serializers
from .models import *

class CurrencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
                'id',
                'currency_name',
                'currency_symbol',
                'currency_rate',
                'is_default'
                ]