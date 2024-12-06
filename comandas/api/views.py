from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from comandas.api.permissions import IsComensalApp, IsAllowedIP
from comandas.models import Categorias, Producto, Pedidos, Comandas, Comensales, Mesa
from comandas.api.serializers import (
    CategoriasSerializer, ProductoSerializer, PedidosSerializer,
    ComandasSerializer, ComensalesSerializer, MesaSerializer, SolcitudesSerializer

)
import uuid
from comensal.models import Solicitudes

# Categorías ViewSet
class CategoriasViewset(ModelViewSet):
    queryset = Categorias.objects.filter(activo=True)
    serializer_class = CategoriasSerializer
    permission_classes = [IsComensalApp, IsAllowedIP]
   
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Solicitudes ViewSet
class SolicitudesViewset(ModelViewSet):
    queryset = Solicitudes.objects.filter(estado=0)
    serializer_class  =SolcitudesSerializer
    permission_classes = [IsAuthenticated]
   
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# Producto ViewSet
class ProductoViewset(ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [IsComensalApp, IsAllowedIP]

    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True)
        categoria_id = self.request.query_params.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset


# Pedidos ViewSet
class PedidosViewset(ModelViewSet):
    serializer_class = PedidosSerializer
    permission_classes = [IsComensalApp, IsAllowedIP]

    def get_queryset(self):
        """
        Filtrar pedidos según los parámetros proporcionados en la URL y el comensal autenticado.
        """
        try:
            # Obtener el comensal desde el token
            comensal = Comensales.objects.get(token=self.request.headers.get("Authorization").split("Bearer ")[-1])
        except Comensales.DoesNotExist:
            raise NotAuthenticated("Token no válido o comensal no encontrado")

        queryset = Pedidos.objects.filter(comensal=comensal)  # Filtrar solo por el comensal autenticado
        comanda_id = self.request.query_params.get('comanda')
        estado = self.request.query_params.get('estado')

        if comanda_id:
            queryset = queryset.filter(comanda_id=comanda_id)
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    @action(detail=False, methods=["post"], url_path="confirmar")
    def confirmar(self, request):
        """
        Cambia el estado de los pedidos de una comanda a 'preparación' (estado 0).
        """
        comanda_id = request.data.get("comanda")
        if not comanda_id:
            return Response({"error": "El campo 'comanda' es obligatorio."}, status=400)

        # Validar el token y obtener el comensal
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            comensal = Comensales.objects.get(token=token)
        except Comensales.DoesNotExist:
            raise NotAuthenticated("Token no válido o comensal no encontrado")

        # Filtrar pedidos
        pedidos = Pedidos.objects.filter(comanda_id=comanda_id, comensal=comensal, estado=4)
        if not pedidos.exists():
            return Response({"error": "No hay pedidos en estado 'confirmar'."}, status=404)

        # Cambiar el estado y guardar
        for pedido in pedidos:
            pedido.estado = 0
            pedido.hora_ini=timezone.now()
            pedido.save()

        return Response({"mensaje": "Pedidos confirmados exitosamente."}, status=200)

  


# Comandas ViewSet
class ComandasViewset(ModelViewSet):
    serializer_class = ComandasSerializer
    permission_classes = [IsComensalApp, IsAllowedIP]

    def get_queryset(self):
        mesa_id = self.request.query_params.get('mesa')
        if mesa_id:
            return Comandas.objects.filter(mesa_id=mesa_id, estado=0)
        return Comandas.objects.none()

    @action(detail=False, methods=['post'])
    def solicitar_atencion(self, request):
        mesa_id = request.data.get('mesa')
        if not mesa_id:
            return Response({'error': 'Mesa es requerida.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'mensaje': 'Solicitud de atención enviada correctamente.'}, status=status.HTTP_200_OK)


# Comensales ViewSet
class ComensalesViewset(ModelViewSet):
    serializer_class = ComensalesSerializer
    permission_classes = [IsComensalApp, IsAllowedIP]

    def create(self, request, *args, **kwargs):
        data = request.data
        comanda_id = data.get("comanda")
        nombre = data.get("nombre", "").strip()
        correo = data.get("correo", "").strip()
        telefono = data.get("telefono", "").strip()

        # Validar que comanda_id esté presente
        if not comanda_id:
            return JsonResponse({'error': 'Comanda es requerida.'}, status=400)

        # Validar campos obligatorios
        if not nombre:
            return JsonResponse({'error': 'El nombre es obligatorio.'}, status=400)

        # Verificar si existe la comanda
        try:
            comanda = Comandas.objects.get(id=comanda_id)
        except Comandas.DoesNotExist:
            return JsonResponse({'error': 'Comanda no encontrada.'}, status=404)

        # Buscar posibles coincidencias por nombre en la misma comanda
        posibles_coincidencias = Comensales.objects.filter(nombre=nombre, comanda=comanda)
        for comensal in posibles_coincidencias:
            comensal_correo = comensal.correo or ""
            comensal_telefono = comensal.telefono or ""

            # Validar si los datos coinciden exactamente
            if correo == comensal_correo and telefono == comensal_telefono:
                return JsonResponse(
                    {'error': 'El comensal ya está registrado con los mismos datos.'},
                    status=400,
                )

        # Generar token único para el comensal
        token = str(uuid.uuid4())
        data['token'] = token

        # Crear el comensal
        serializer = self.get_serializer(data={**data, 'comanda': comanda.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Configurar la cookie
        response = JsonResponse({'mensaje': 'Comensal registrado con éxito'})
        response.set_cookie(
            'comensalToken',
            token,
            httponly=True,
            max_age=3600 * 12  # Expira en 12 horas
        )
        return response


# Mesa ViewSet
class MesaViewset(ModelViewSet):
    queryset = Mesa.objects.filter(activa=True)
    serializer_class = MesaSerializer
    permission_classes = [IsComensalApp, IsAllowedIP]
