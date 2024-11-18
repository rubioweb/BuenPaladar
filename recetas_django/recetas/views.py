from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,ListView,DetailView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Receta,Comentario,Etiqueta
from .forms import RecetaForm, ComentarioForm
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.views import View
from .serializador import RecetaSerializer
from rest_framework import generics


# vista bienvenidasour
class Bienvenidaview(TemplateView):
    template_name = 'recetas/bienvenida.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recetas'] = Receta.objects.all()  # Agregamos todas las recetas al contexto
        return context
    

#vista para iniciar sesion login
class IniciarSesion(LoginView):
    template_name = 'recetas/login.html'
  


#vista para registrarse
class RegistroUsuario(CreateView):
    form_class = UserCreationForm
    template_name = 'recetas/register.html'
    success_url = reverse_lazy('login')


# pa cerrar sesin
class CerrarSesion(LogoutView):
    next_page = 'home'   #retorna pa la vista bienvenida


#vista de todas las recetas
class RecetaListView(ListView): #####aki hay cambio_para que se vean
    model = Receta #modelo que vamos a listar
    template_name = 'recetas/receta_list.html'  # plantilla que se usara para mostrar las recetas
    context_object_name = 'recetas' #nombre del contexto para acceder a las recetas en la plantilla

    #configuración para que solo usuarios autenticados puedan ver esta vista
    #login_url = 'login'  # URL a la que se redirige si el usuario no está autenticado


# los detalles de una receta
class RecetaDetailView(DetailView): ##########
    model = Receta
    template_name = 'recetas/receta_detalle.html'
    context_object_name = 'receta' 

    # Sobrescribimos el metodo get_context_data para incluir el formulario de comentarios
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['form'] = ComentarioForm()  #agregamos el formulario de comentarios al contexto
        context['comentarios'] = self.object.comentarios.all()  # cargamos los comentarios de la receta

             # Si el usuario está autenticado, mostramos el formulario de comentarios
        if self.request.user.is_authenticated:
            context['form'] = ComentarioForm()  #agregamos el formulario de comentarios al contexto
        else:
            context['form'] = None  # No mostramos el formulario si no está autenticado

        return context      

    #sobrescribimos el metodo post para manejar el envío de formularios de comentarios
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  #obtenemos la receta actual
        form = ComentarioForm(request.POST)

                # Si el usuario no está autenticado, mostramos un mensaje para que inicie sesión
        if not request.user.is_authenticated:
            messages.warning(request, "Regístrate o inicia sesión para dejar un comentario.")
            return redirect('login')

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.receta = self.object #asociamos el comentario a la receta actual
            comentario.autor = request.user # el autor del comentario es el usuario autenticado
            comentario.save()#guardamos el comentario
            return redirect(reverse('receta_detalle', kwargs={'pk': self.object.pk}))  #redirigimos a la misma pagina de detalles

        #si el formulario no es válido, volvemos a renderizar la pagina con los errores
        context = self.get_context_data()
        context['form'] = form #pasamos el formulario con los errores
        return self.render_to_response(context)
    
     #contador de visitas   (python manage.py recetas_populare)

    def get_object(self, queryset=None):
        receta = super().get_object(queryset)
        
        #incrementar el conteo de visitas
        receta.visitas += 1
        receta.save()

        return receta




'''
# detalles de las recetas
class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'recetas/receta_detalle.html'
    context_object_name = 'receta'
'''


#vista para crear una receta
class RecetaCrearView(LoginRequiredMixin, CreateView):
    model = Receta
    form_class = RecetaForm  #esto hay que importarlo
    template_name = 'recetas/receta_form.html'
    success_url = reverse_lazy('recetas')  #redirige a la lista de recetas después de crear una receta
    login_url = 'login'   #redirige a la vista de login 

    def form_valid(self, form):
        form.instance.autor = self.request.user #asignar el usuario autenticado como el creador de la receta
        return super().form_valid(form)
    


#mis recetas

class MisRecetasListView(LoginRequiredMixin, ListView):
    model = Receta
    template_name = 'recetas/mis_recetas.html'
    context_object_name = 'recetas'
    login_url = 'login'  #redirige a login

    def get_queryset(self):
        #filtra las recetas por el usuario autenticado
        return Receta.objects.filter(autor=self.request.user)
    

#vista para buscar recetas por etiquetas

class BuscarRecetasPorEtiqueta(ListView):
    model = Receta
    template_name = 'recetas/buscar_resultados.html'
    context_object_name = 'recetas'

    def get_queryset(self):
        etiqueta_id = self.request.GET.get('etiqueta')
        if etiqueta_id:
            return Receta.objects.filter(etiquetas__id=etiqueta_id)
        return Receta.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etiquetas'] = Etiqueta.objects.all()
        return context
    

    #vista para editar receta
class RecetaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/receta_form.html'
    success_url = reverse_lazy('mis_recetas')

    # Verificar que el usuario que intenta editar sea el autor de la receta
    def test_func(self):
        receta = self.get_object()
        return self.request.user == receta.autor



    # vista para borrar la receta

class RecetaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
        
    model = Receta
    template_name = 'recetas/receta_confirm_delete.html'
    success_url = reverse_lazy('mis_recetas')

    # Verificar que el usuario que intenta eliminar sea el autor de la receta
    def test_func(self):
        receta = self.get_object()
        return self.request.user == receta.autor

# vista para dar me_gusta

class DarMeGusta(View):
    def post(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)

        if request.user in receta.me_gusta.all():
            receta.me_gusta.remove(request.user)  # Si ya dio "me gusta", lo quitamos
        else:
            receta.me_gusta.add(request.user)  # Si no, agregamos el "me gusta"

        return redirect('receta_detalle', pk=receta.id)
    

# API   http://localhost:8000/api/recetas/
 
class RecetaListAPIView(generics.ListAPIView):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer
