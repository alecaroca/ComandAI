from rest_framework import serializers
from comandas.models import User, Categorias, Producto, Pedidos, Comandas, Comensales, Mesa
from comensal.models import Solicitudes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'is_staff']


class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = ['id', 'nombre', 'descripcion', 'imagen']


class ProductoSerializer(serializers.ModelSerializer):
    precio_format = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 
            'nombre', 
            'descripcion', 
            'precio', 
            'precio_format', 
            'tiempo', 
            'activo', 
            'categoria', 
            'imagen'
        ]

    def get_precio_format(self, obj):
        # Formatear el precio con separador de miles y estilo pesos chilenos
        return f"${obj.precio*1.19:,.0f}".replace(",", ".")  # Ejemplo: $1.000

class PedidosSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_precio_format = serializers.SerializerMethodField()
    total_pedido_format = serializers.SerializerMethodField()

    def get_producto_precio_format(self, obj):
        return f"${obj.producto.precio:,.0f}".replace(",", ".")

    def get_total_pedido_format(self, obj):
        # Formatear el total del pedido para visualización
        total = obj.cantidad * obj.producto.precio
        return f"${total*1.19:,.0f}".replace(",", ".")

    class Meta:
        model = Pedidos
        fields = ['id', 'producto', 'producto_nombre', 'producto_precio_format', 
                  'cantidad', 'total_pedido', 'total_pedido_format', 'estado', 
                  'comanda', 'comensal']




class ComandasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comandas
        fields = ['id', 'mesa', 'estado', 'fecha_ini', 'fecha_fin', 'notas']


class ComensalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comensales
        fields = ['id', 'nombre', 'correo', 'telefono', 'comanda', "token"]


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ['id', 'numero_mesa', 'estado', 'activa']

class SolcitudesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitudes
        fields = '__all__'
