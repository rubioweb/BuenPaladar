from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Receta, Etiqueta, Comentario

#clase personalizada para el modelo Receta
@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fecha_creacion', 'dificultad')
    search_fields = ('nombre', 'ingredientes', 'categoria')
    list_filter = ('categoria', 'dificultad', 'fecha_creacion')

# clase personalizada para el modelo Etiqueta
@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# clase personalizada para el modelo Comentario
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'receta', 'fecha_creacion')
    search_fields = ('autor__username', 'contenido')
    list_filter = ('fecha_creacion',)
