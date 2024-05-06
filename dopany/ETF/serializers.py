# serializers.py

from rest_framework import serializers
from .models import Etf, EtfMajorCompany, Domain

class Domain(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class EtfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etf
        fields = '__all__'


class EtfMajorCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = EtfMajorCompany
        fields = '__all__'
        

