from django import forms
from .models import Receta,Comentario
#from .models import Comentario

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'ingredientes', 'elaboracion', 'tiempo_preparacion', 'comensales', 'dificultad', 'imagen', 'etiquetas']
        widgets = {
            'ingredientes': forms.Textarea(attrs={'rows': 4}),
            'elaboracion': forms.Textarea(attrs={'rows': 6}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']  # Solo necesitamos el campo de texto para el comentario
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe un comentario...'}),
        }
        labels = {
            'texto': 'Comentario',
        }