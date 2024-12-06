from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from comandas.api.views import (
    CategoriasViewset, ProductoViewset, PedidosViewset,
    ComandasViewset, ComensalesViewset, MesaViewset, SolicitudesViewset
)

# APIS
router = DefaultRouter()
router.register('categorias', CategoriasViewset, basename='categorias')
router.register('productos', ProductoViewset, basename='productos')
router.register('pedidos', PedidosViewset, basename='pedidos')
router.register('comandas', ComandasViewset, basename='comandas')
router.register('comensales', ComensalesViewset, basename='comensales')
router.register('mesas', MesaViewset, basename='mesas')
router.register('solicitudes', SolicitudesViewset, basename='soliciutdes')

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
