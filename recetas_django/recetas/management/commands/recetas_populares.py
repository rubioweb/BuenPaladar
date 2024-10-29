from django.core.management.base import BaseCommand
from recetas.models import Receta

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # obtener las recetas ordenadas por el campo de visitas, de mayor a menor
        recetas_populares = Receta.objects.order_by('-visitas')[:10]  # para ajustar el número de recetas en la salida

        if recetas_populares:
            self.stdout.write(self.style.SUCCESS('Recetas más populares:'))
            for receta in recetas_populares:
                self.stdout.write(f'- {receta.nombre} ({receta.visitas} visitas)')
        else:
            self.stdout.write(self.style.WARNING('No hay recetas disponibles.'))