from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from comandas.models import User
from .models import Categorias, Producto, Mesa, Comandas, Sucursal, Comensales, Pedidos

@admin.register(User) 
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(Categorias)
admin.site.register(Producto)
admin.site.register(Mesa)

admin.site.register(Comandas)
admin.site.register(Sucursal)
admin.site.register(Comensales)
#admin.site.register(Pedidos)
# Register your models here.

from django.contrib import admin
from .models import Pedidos

from django.contrib import admin
from .models import Pedidos

class PedidosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cantidad', 'total_pedido', 'estado', 'comanda', 'comensal', 'producto', 'notas', 'hora_ini', 'hora_fin')
    list_filter = ('estado', 'comanda', 'producto', 'hora_ini', 'hora_fin')
    search_fields = ('id', 'comanda__id', 'producto__nombre', 'comensal__nombre', 'notas')
    readonly_fields = ('hora_ini', 'hora_fin')
    fieldsets = (
        (None, {
            'fields': ('cantidad', 'total_pedido', 'estado', 'comanda', 'comensal', 'producto', 'notas')
        }),
        ('Tiempos', {
            'fields': ('hora_ini', 'hora_fin'),
        }),
    )

admin.site.register(Pedidos, PedidosAdmin)

