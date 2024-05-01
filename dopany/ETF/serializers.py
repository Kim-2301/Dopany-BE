# serializers.py

from rest_framework import serializers
from .models import Etf

class EtfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etf
        fields = ['transaction_date', 'closing_price']
        

