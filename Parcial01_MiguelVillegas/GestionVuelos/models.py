from django.db import models

# Create your models here.
class Vuelo (models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20)
    precio = models.IntegerField()
