from rest_framework import serializers
from rutas.models import Rutas

class RutasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rutas
        fields = '__all__'
