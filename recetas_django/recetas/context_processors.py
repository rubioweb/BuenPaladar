from .models import Etiqueta

def etiquetas_disponibles(request):
    return {
        'etiquetas': Etiqueta.objects.all()
    }