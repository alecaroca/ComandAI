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
    imagen = models.ImageField(upload_to="productos", null=True)
    tiempo = models.TimeField(blank=True, null=True)

    def __str__(self): 
        return self.nombre 


ubicacion=[
    [0,'1er piso'],
    [1,'2er piso'],
    [2,'3er piso'],
    [3,'terraza']
]

estados_mesas=[

    [0,'Libre'],
    [1,'Ocupado'],

]

class Sucursal(models.Model):
    nombre_sucursal = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return self.nombre_sucursal
    
class Mesa(models.Model):
    numero_mesa = models.IntegerField()
    mesero = models.ForeignKey(User, on_delete =models.PROTECT)
    activa = models.BooleanField()
    capacidad  = models.IntegerField(blank=True, null=True)
    ubicacion = models.IntegerField(choices=ubicacion, blank=True, null=True)
    estado = models.IntegerField(choices=estados_mesas, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete = models.PROTECT, blank=True, null=True)

    def __int__(self): 
        return self.numero_mesa 

estado_comandas=[
    [0,'Abierta'],
    [1,'Cerrada'],
]
medio_pago=[
    [0,'Efectivo'],
    [1,'Transferencia'],
    [2,'Tarjetas'],
]
class Comandas(models.Model):
    fecha_ini = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    valor_neto = models.IntegerField(blank=True, null=True)
    iva = models.IntegerField(blank=True, null=True)
    descuento = models.IntegerField(blank=True, null=True)
    sub_total = models.IntegerField(blank=True, null=True)
    propina = models.IntegerField(blank=True, null=True)
    abono = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    estado = models.IntegerField(choices=estado_comandas)
    notas = models.TextField(blank=True, null=True)
    medio_pago = models.IntegerField(choices=medio_pago,blank=True, null=True)
    mesero = models.ForeignKey(User, on_delete =models.PROTECT)
    mesa = models.ForeignKey(Mesa, on_delete= models.PROTECT)

    def __int__(self): 
        return self.id

class Comensales(models.Model):
    nombre = models.CharField(max_length=30,blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=12,blank=True, null=True)
    comanda = models.ForeignKey(Comandas, on_delete= models.PROTECT,blank=True, null=True )
    token = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.nombre or "Comensal sin nombre"

estado_pedido = [
    (0, 'preparacion'),
    (1, 'entregado'),
    (2, 'preparado'),
    (3, 'marcado'),
    (4, 'confirmar'),
]

class Pedidos(models.Model):
    cantidad = models.IntegerField(blank=True, null=True)
    total_pedido = models.IntegerField(blank=True, null=True)
    estado =models.IntegerField(choices=estado_pedido, blank=True, null=True)
    comanda = models.ForeignKey(Comandas, on_delete=models.PROTECT, blank=True, null=True, related_name="pedidos")
    comensal = models.ForeignKey(Comensales, on_delete=models.PROTECT, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    hora_ini = models.DateTimeField(auto_now_add=True)  
    hora_fin = models.DateTimeField(blank=True, null=True)

    def __int__(self):
        return self.id




