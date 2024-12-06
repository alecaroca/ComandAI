from django.contrib import admin
from .models import Solicitudes

@admin.register(Solicitudes)
class SolicitudesAdmin(admin.ModelAdmin):
    # Campos visibles en la lista del administrador
    list_display = ('tipo', 'estado', 'mesa', 'fecha_creacion')  # Elimina 'fecha_actualizacion'
    
    # Filtros para facilitar la búsqueda
    list_filter = ('estado', 'tipo')
    
    # Campos que serán buscables
    search_fields = ('mesa__numero_mesa', 'tipo')
    
    # Ordenar por fecha de creación (descendente)
    ordering = ('-fecha_creacion',)
