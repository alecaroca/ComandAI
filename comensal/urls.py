from django.urls import path
from .views import ingreso_comensal, RegistrarComensalView, ConsultarEstadoSolicitudView, error_acceso,menu_comensal,confirmar_pedido,pedidos_comensal,solicitar_atencion

urlpatterns = [
    path('ingreso/', ingreso_comensal, name='ingreso_comensal'),
    path('registrar_comensal/', RegistrarComensalView.as_view(), name='registrar_comensal'),
    path('consultar_estado_solicitud/<int:solicitud_id>/', ConsultarEstadoSolicitudView.as_view(), name='consultar_estado_solicitud'),
    path('menu/', menu_comensal, name='menu_comensal'),
    path('confirmar-pedido/', confirmar_pedido, name='confirmar_pedido'),
    path('mis-pedidos/', pedidos_comensal, name='mis_pedidos'),
    path('solicitar-atencion/', solicitar_atencion, name='solicitar_atencion'),
    path('error-acceso/', error_acceso, name='error_acceso'),
]



"""from django.urls import path
from .views import ingreso,menu_categorías,menu_productos


urlpatterns = [
    path('ingreso/', ingreso, name="ingreso"),
    path('menu_categorías/', menu_categorías, name="menu_categorías"),
    path('menu_productos/<id>/', menu_productos, name="menu_productos"),
    ]

"""