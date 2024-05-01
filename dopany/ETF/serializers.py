from rest_framework import serializers
from .models import Etf, EtfMajorCompany, Domain

class Domain(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'