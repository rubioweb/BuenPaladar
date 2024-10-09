from django.urls import path
from .views import Bienvenidaview,IniciarSesion,RegistroUsuario,RecetaListView


urlpatterns =[

    path('',Bienvenidaview.as_view(), name='home'),
    path('login/',IniciarSesion.as_view(), name='login' ),
    path('register/', RegistroUsuario.as_view(), name = 'register'),
    path('recetas/',RecetaListView.as_view(), name = 'recetas')
]