from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,ListView,DetailView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Receta
from .forms import RecetaForm, ComentarioForm


# vista bienvenida

class Bienvenidaview(TemplateView):
    template_name = 'recetas/bienvenida.html'

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
class RecetaListView(LoginRequiredMixin, ListView):
    model = Receta #modelo que vamos a listar
    template_name = 'recetas/receta_list.html'  # plantilla que se usara para mostrar las recetas
    context_object_name = 'recetas' #nombre del contexto para acceder a las recetas en la plantilla

    #configuración para que solo usuarios autenticados puedan ver esta vista
    login_url = 'login'  # URL a la que se redirige si el usuario no está autenticado



class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'recetas/receta_detalle.html'
    context_object_name = 'receta' #nombre que usaremos en la plantilla para acceder a la receta

    # Sobrescribimos el metodo get_context_data para incluir el formulario de comentarios
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()  #agregamos el formulario de comentarios al contexto
        context['comentarios'] = self.object.comentarios.all()  # cargamos los comentarios de la receta
        return context

    #sobrescribimos el metodo post para manejar el envío de formularios de comentarios
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  #obtenemos la receta actual
        form = ComentarioForm(request.POST)

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

    def form_valid(self, form):
        form.instance.autor = self.request.user #asignar el usuario autenticado como el creador de la receta
        return super().form_valid(form)
    


#mis recetas

class MisRecetasListView(LoginRequiredMixin, ListView):
    model = Receta
    template_name = 'recetas/mis_recetas.html'
    context_object_name = 'recetas'

    def get_queryset(self):
        #filtra las recetas por el usuario autenticado
        return Receta.objects.filter(autor=self.request.user)
    

