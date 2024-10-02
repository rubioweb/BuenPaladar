from django.db import models
from django.contrib.auth.models import User


# modelo para etiquetar recetas de manera flexible
class Etiqueta(models.Model):
    # campo para el nombre de la etiqueta, unico para evitar duplicados
    nombre = models.CharField(max_length=100, unique=True)
    # campo opcional para describir la etiqueta
    descripcion = models.TextField(blank=True, null=True)

    # metodo que devuelve una representación en cadena del objeto
    def __str__(self):
        return self.nombre

# MODELO PARA REPRESENTAR UNA RECETA
class Receta(models.Model):
    nombre = models.CharField(max_length=255)# nombre de la receta
    ingredientes = models.TextField() #lista de ingredientes para la receta
    elaboracion = models.TextField()  #instrucciones para elaborar la receta
    tiempo_preparacion = models.PositiveIntegerField(help_text='Tiempo en minutos')#tiempo de preparación en minutos
    # numero de personas para las que está pensada la receta
    comensales = models.PositiveIntegerField(help_text='Número de personas para las que se prepara la receta')
    dificultad = models.CharField(   #dificultad de la receta, con opciones predeterminadas
        max_length=50, 
        choices=[('Fácil', 'Fácil'), ('Media', 'Media'), ('Difícil', 'Difícil')]
    )
    
    categoria = models.CharField(max_length=100) # categoría de la receta (por ejemplo, "Postre", "Entrante")
    # relacion de muchos a muchos con el modelo Etiqueta para clasificar recetas
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='recetas')
    # campo para cargar una imagen de la receta
    imagen = models.ImageField(upload_to='recetas_imagenes/', blank=True, null=True)
    #fecha y hora en que la receta fue creada, automáticamente asignada
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    #autor de la receta, vinculado al modelo de usuario de Django
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas')

    #metodo que devuelve una representacion en cadena del objeto
    def __str__(self):
        return self.nombre

#modelo para representar comentarios en las recetas
class Comentario(models.Model):
    #la receta a la que pertenece el comentario
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE) #el autor del comentario, vinculado al usuario
    texto = models.TextField()# Texto del comentario
    fecha_creacion = models.DateTimeField(auto_now_add=True)#fecha/hora en que el comentario fue creado, automaticamente asignada

    #metodo que devuelve una representacion en cadena del objeto
    def __str__(self):
        return f'Comentario de {self.autor.username} sobre {self.receta.nombre}'
