# serializers.py

from rest_framework import serializers
from .models import Industry, Company, Domain

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
        



class Industry(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'
        
class Company(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'