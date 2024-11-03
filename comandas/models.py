from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=[]

class Categorias(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    activo = models.BooleanField()
    imagen = models.ImageField(upload_to="categorias", null=True)

    def __str__(self): 
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    descripcion = models.TextField()
    activo = models.BooleanField()
    categoria = models.ForeignKey(Categorias, on_delete =models.PROTECT)
    fecha_modificacion = models.DateField
    imagen = models.ImageField(upload_to="productos", null=True)

    def __str__(self): 
        return self.nombre 
    
class Mesa(models.Model):
    numero_mesa = models.IntegerField()
    mesero = models.ForeignKey(User, on_delete =models.PROTECT)
    activa = models.BooleanField()