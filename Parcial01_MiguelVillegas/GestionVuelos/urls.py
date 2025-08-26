from django.urls import path
from .views import HomePageView, RegistrarVueloView, VueloListView, EstadisticasView


urlpatterns = [
    path("", HomePageView.as_view(), name = 'home'),
    path("registrar/", RegistrarVueloView.as_view(), name = 'registrar'),
    path("listar/", VueloListView.as_view(), name = 'listar'),
    path("estadisticas/", EstadisticasView.as_view(), name = 'estadisticas'),
]