from rest_framework import serializers
from .models import Receta

# recetas/serializers.py

class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = ['id', 'nombre', 'ingredientes', 'dificultad', 'imagen'] 