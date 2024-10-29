from django.urls import path
from .views import Bienvenidaview,IniciarSesion,RegistroUsuario,CerrarSesion,RecetaListView,RecetaDetailView,RecetaCrearView,MisRecetasListView,BuscarRecetasPorEtiqueta,RecetaUpdateView,RecetaDeleteView


urlpatterns =[

    path('',Bienvenidaview.as_view(), name='home'),
    path('login/',IniciarSesion.as_view(), name='login' ),
    path('register/', RegistroUsuario.as_view(), name = 'register'),
    path('logout',CerrarSesion.as_view(), name = 'logout'),
    path('recetas/',RecetaListView.as_view(), name = 'recetas'),
    path('recetas/<int:pk>/', RecetaDetailView.as_view(), name = 'receta_detalle'),
    path('crear',RecetaCrearView.as_view(), name='receta_crear'),
    path('mis_recetas',MisRecetasListView.as_view(), name='mis_recetas' ),
    path('buscar-etiquetas/',BuscarRecetasPorEtiqueta.as_view(), name='buscar_etiquetas' ),
    path('receta/<int:pk>/editar/', RecetaUpdateView.as_view(), name='receta_editar'),
    path('receta/<int:pk>/eliminar/', RecetaDeleteView.as_view(), name='receta_eliminar'),


]