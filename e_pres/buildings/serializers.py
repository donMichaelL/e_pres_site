from rest_framework import serializers
from .models import Building

class BuildingSerializer(serializers.ModelSerializer):
    # country = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = '__all__'

    # def get_country(self, obj):
    #     return obj.get_country_display()
