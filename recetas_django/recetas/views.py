from django.shortcuts import render
from django.views.generic import TemplateView,CreateView,ListView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Receta  


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

#vista de las recetas
class RecetaListView(LoginRequiredMixin, ListView):
    model = Receta #modelo que vamos a listar
    template_name = 'recetas/receta_list.html'  # plantilla que se usara para mostrar las recetas
    context_object_name = 'recetas' #nombre del contexto para acceder a las recetas en la plantilla

    #configuración para que solo usuarios autenticados puedan ver esta vista
    login_url = 'login'  # URL a la que se redirige si el usuario no está autenticado
