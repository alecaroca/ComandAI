# Modelo para gestionar las solicitudes de acceso de comensales y atención
from django.db import models
from comandas.models import Mesa  # Importar desde la app comandas

class Solicitudes(models.Model):
    TIPO_SOLICITUD = [
        ('comensal', 'Acceso de Comensal'),
        ('atencion', 'Solicitud de Atención'),
    ]

    ESTADO_SOLICITUD = [
        (0, 'Pendiente'),
        (1, 'Aprobado'),
        (2, 'Rechazado'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_SOLICITUD)
    estado = models.IntegerField(choices=ESTADO_SOLICITUD, default=0)
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, null=True, blank=True)  # No es obligatorio
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - Estado: {self.get_estado_display()}"


