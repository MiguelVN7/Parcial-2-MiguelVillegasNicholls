from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.db import models
from .models import Vuelo
from django.core.exceptions import ValidationError

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'GestionVuelos/home.html'

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ['nombre', 'tipo', 'precio']

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if tipo:
            tipo_lower = tipo.lower().strip()
            if tipo_lower not in ['nacional', 'internacional']:
                raise ValidationError("El tipo debe ser 'nacional' o 'internacional'.")
            return tipo_lower.capitalize() 
        return tipo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio <= 0:
                raise ValidationError("El precio debe ser mayor a 0.")
            if precio > 999999999:  
                raise ValidationError("El precio no puede ser mayor a 999,999,999.")
        return precio

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            if len(nombre) < 2:
                raise ValidationError("El nombre debe tener al menos 2 caracteres.")
            if len(nombre) > 255:
                raise ValidationError("El nombre no puede tener más de 255 caracteres.")
        return nombre

# Product Create Page
class RegistrarVueloView(TemplateView):
    template_name = 'GestionVuelos/registrar.html'

    def get(self, request):
        form = VueloForm()
        viewData = {}
        viewData["title"] = "Registrar Vuelo"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = VueloForm(request.POST)
        if form.is_valid():
            vuelo = form.save()
            return redirect('home')  # Redirigir al home después de guardar
        else:
            viewData = {}
            viewData["title"] = "Registrar Vuelo"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        

class VueloListView(ListView):
    model = Vuelo
    template_name = 'GestionVuelos/lista_vuelos.html'
    context_object_name = 'vuelos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vuelos Registrados - Alcaldía Rionegro'
        context['subtitle'] = 'Lista de Vuelos'
        return context
    
class EstadisticasView(TemplateView):
    template_name = 'GestionVuelos/estadisticas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contar vuelos nacionales e internacionales
        vuelos_nacionales = Vuelo.objects.filter(tipo__iexact='nacional').count()
        vuelos_internacionales = Vuelo.objects.filter(tipo__iexact='internacional').count()
        total_vuelos = vuelos_nacionales + vuelos_internacionales
        
        # Calcular porcentajes
        if total_vuelos > 0:
            porcentaje_nacionales = round((vuelos_nacionales / total_vuelos) * 100, 1)
            porcentaje_internacionales = round((vuelos_internacionales / total_vuelos) * 100, 1)
        else:
            porcentaje_nacionales = 0
            porcentaje_internacionales = 0
        
        # Calcular precio promedio de vuelos nacionales
        vuelos_nacionales_query = Vuelo.objects.filter(tipo__iexact='nacional')
        if vuelos_nacionales_query.exists():
            precio_promedio_nacional = vuelos_nacionales_query.aggregate(
                promedio=models.Avg('precio')
            )['promedio']
        else:
            precio_promedio_nacional = 0
        
        context.update({
            'title': 'Estadísticas de Vuelos',
            'subtitle': 'Resumen de Vuelos Registrados',
            'vuelos_nacionales': vuelos_nacionales,
            'vuelos_internacionales': vuelos_internacionales,
            'total_vuelos': total_vuelos,
            'porcentaje_nacionales': porcentaje_nacionales,
            'porcentaje_internacionales': porcentaje_internacionales,
            'precio_promedio_nacional': precio_promedio_nacional,
        })
        
        return context
