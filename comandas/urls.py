from django.urls import path, include
from .views import login, usuarios, productos, categorias, mesas, exit, agregar_productos, modificar_productos, eliminar_producto,agregar_usuario,eliminar_usuario, modificar_usuario, agregar_categorias, modificar_categorias,eliminar_categorias, agregar_mesas, eliminar_mesas, modificar_mesas, preparacion, actualizar_comandas, comandas, listarcomandas, detallecomandas, agregarpedido, nuevacomanda, eliminar_producto,agregar_usuario,eliminar_usuario, modificar_usuario, agregar_categorias, modificar_categorias,eliminar_categorias, agregar_mesas, eliminar_mesas, modificar_mesas, preparacion, actualizar_comandas, comandas, listarcomandas, detallecomandas, actualizar_estado_pedido, marcar_comanda_preparada,desglosecuenta,eliminar_pedido, mismesas



urlpatterns = [
    path('', usuarios, name="usuarios"),
    path('usuarios/', usuarios, name="usuarios"),
    path('productos/', productos, name="productos"),
    path('categorias/', categorias, name="categorias"),
    path('mesas/', mesas, name="mesas"),
    
    path('logout/', exit, name="exit"),

    path('agregar-productos/', agregar_productos, name="agregar_productos"),
    path('modificar-productos/<id>/', modificar_productos, name="modificar_productos"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),

    path('agregar-usuario/', agregar_usuario, name="agregar_usuario"),
    path('eliminar-usuario/<id>/', eliminar_usuario, name="eliminar_usuario"),
    path('modificar-usuario/<id>/', modificar_usuario, name="modificar_usuario"),

    path('agregar-categorias/', agregar_categorias, name="agregar_categorias"),
    path('eliminar-categorias/<id>/', eliminar_categorias, name="eliminar_categorias"),
    path('modificar-categorias/<id>/', modificar_categorias, name="modificar_categorias"),

    path('agregar-mesas/', agregar_mesas, name="agregar_mesas"),
    path('eliminar-mesas/<id>/', eliminar_mesas, name="eliminar_mesas"),
    path('modificar-mesas/<id>/', modificar_mesas, name="modificar_mesas"),

    path('preparacion/', preparacion, name='preparacion'),
    path('preparacion/actualizar/', actualizar_comandas, name='actualizar_comandas'),
    path('preparacion/actualizar-estado-pedido/<int:pedido_id>/', actualizar_estado_pedido, name='actualizar_estado_pedido'),
    path('preparacion/marcar-comanda-preparada/<int:comanda_id>/', marcar_comanda_preparada, name='marcar_comanda_preparada'),

    path('comandas/', comandas, name="comandas"),
    path('listarcomandas/<id>/', listarcomandas, name="listarcomandas"),
    path('detallecomandas/<id>/<det>/', detallecomandas, name="detallecomandas"),
    path('agregarpedido/<comanda>/<id>', agregarpedido, name="agregarpedido"),
    path('nuevacomanda/', nuevacomanda, name="nuevacomanda"),
    path('desglosecuenta/<id>/', desglosecuenta, name="desglosecuenta"),
    path('eliminar-pedido/<id>/<idcomanda>/', eliminar_pedido, name="eliminar_pedido"),
    path('mismesas/<id>/', mismesas, name="mismesas"),
    path('comensal/', include('comensal.urls')),  # Incluir las rutas de la app comensal
    


 

   
]