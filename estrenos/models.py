from django.db import models
from django.db.models.fields import CharField

# Create your models here.


class Usuario(models.Model):
    usuario = CharField(max_length=16)
    password = CharField(max_length=16)


class Pelicula(models.Model):
    titulo = CharField(unique=True, primary_key=True, max_length=50)
    descripcion = CharField(max_length=500)
    imagen = CharField(max_length=100)
    link = CharField(max_length=100)
    usuarios = models.ManyToManyField(Usuario, blank=True)
