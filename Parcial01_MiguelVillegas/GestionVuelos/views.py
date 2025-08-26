from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Vuelo
from django.core.exceptions import ValidationError

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'GestionVuelos/home.html'

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ['nombre', 'tipo', 'precio']

    def validarTipo(self):
        tipo = self.cleaned_data.get('price')
        if tipo.lower() != 'nacional' or 'internacional': 
            raise ValidationError("El tipo debe ser nacional o internacional.")
        return tipo

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