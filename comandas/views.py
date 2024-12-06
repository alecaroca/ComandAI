from comandas.api.serializers import UserSerializer
from urllib import request, response
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import User, Producto, Categorias, Mesa, Comandas, Pedidos,Comensales
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from .forms import ProductoForm, CustomUserCreationForm, CategoriasForm, MesaForm, ComandasForm, MesaupdateForm,ComensalForm, agregarpedidoForm,updatepedidoForm, cierrecomandaForm
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.utils import timezone
import json
from django.db.models import Avg, Count, Min, Sum,  F, FloatField, Func,IntegerField
from comensal.models import Solicitudes


def login(request):
    return render(request,'registration/login.html')
    
@login_required
def usuarios(request):
    usuarios = User.objects.all()
    data = {
        'usuarios': usuarios
    }
    
    return render(request,'comandas/usuarios/usuarios.html',data)

@login_required
def productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    print(productos[1]) 
    return render(request,'comandas/productos/productos.html',data)

@login_required
def categorias(request):
    categorias = Categorias.objects.all()
    data = {
        'categorias': categorias
    }
    print(categorias[1]) 
    return render(request,'comandas/categorias/categorias.html',data)

@login_required
def mesas(request):
    mesas = Mesa.objects.all()
    data = {
        'mesas': mesas
    }
    print(mesas[1]) 
    return render(request,'comandas/mesas/mesas.html',data)

def exit(request):
    logout(request)
    return redirect('login')


#CRUD PRODUCTOS
@permission_required('app.add_productos')
def agregar_productos(request):
    data ={
        'form' : ProductoForm()
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Agregado correctamente")
            return redirect(to="productos")
        else: 
            data["form"] = formulario
    

    return render(request, 'comandas/productos/agregar.html',data)

@permission_required('app.change_productos')
def modificar_productos(request, id):
    producto = get_object_or_404(Producto, id=id)
    data ={
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="productos")
        data["form"] = formulario

    return render(request, 'comandas/productos/modificar.html', data)

@permission_required('app.delete_productos')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto,id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to='productos')

#CRUD USUARIOS

def agregar_usuario(request):
    data ={
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Eliminado correctamente")
            return redirect(to='usuarios')
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def eliminar_usuario(request, id):
    producto = get_object_or_404(User,id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to='usuarios')

def modificar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    data ={
        'form': CustomUserCreationForm(instance=usuario)
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST, instance=usuario, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="usuarios")
        data["form"] = formulario

    return render(request, 'comandas/usuarios/modificar.html', data)

#CRUD CATEGORIAS


def agregar_categorias(request):
    data ={
        'form' : CategoriasForm()
    }
    
    if request.method == 'POST':
        formulario = CategoriasForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Agregado correctamente")
            return redirect(to="categorias")
        else: 
            data["form"] = formulario
    

    return render(request, 'comandas/categorias/agregar.html',data)


def modificar_categorias(request, id):
    categorias = get_object_or_404(Categorias, id=id)
    data ={
        'form': CategoriasForm(instance=categorias)
    }

    if request.method == 'POST':
        formulario = CategoriasForm(data=request.POST, instance=categorias, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="categorias")
        data["form"] = formulario

    return render(request, 'comandas/categorias/modificar.html', data)


def eliminar_categorias(request, id):
    categorias = get_object_or_404(Categorias,id=id)
    categorias.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to='categorias')

#CRUD MESAS

def agregar_mesas(request):
    data ={
        'form' : MesaForm()
    }
    
    if request.method == 'POST':
        formulario = MesaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Agregado correctamente")
            return redirect(to="mesas")
        else: 
            data["form"] = formulario
    

    return render(request, 'comandas/mesas/agregar.html',data)


def modificar_mesas(request, id):
    mesas = get_object_or_404(Mesa, id=id)
    data ={
        'form': MesaForm(instance=mesas)
    }

    if request.method == 'POST':
        formulario = MesaForm(data=request.POST, instance=mesas, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="mesas")
        data["form"] = formulario

    return render(request, 'comandas/mesas/modificar.html', data)


def eliminar_mesas(request, id):
    mesas = get_object_or_404(Mesa,id=id)
    mesas.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to='mesas')


#######################################################################################
# INICIO Módulo de preparación para Cocina o barra
#######################################################################################

# Renderiza la página principal del módulo de preparación
@login_required
def preparacion(request):
    comandas = Comandas.objects.filter(pedidos__estado__in=[0, 3]).distinct().prefetch_related('pedidos__producto', 'pedidos__comensal')

    datos_comandas = []
    for comanda in comandas:
        pedidos = comanda.pedidos.filter(estado__in=[0, 3])  # Solo pedidos en preparación o marcados
        total_pedidos = pedidos.count()
        pedidos_preparados = comanda.pedidos.filter(estado=3).count()

        # Calcular tiempo transcurrido desde el primer pedido
        primer_pedido = pedidos.order_by('hora_ini').first()
        tiempo_transcurrido = "00:00"
        if primer_pedido and primer_pedido.hora_ini:
            delta = now() - primer_pedido.hora_ini
            minutos = delta.total_seconds() // 60
            segundos = delta.total_seconds() % 60
            tiempo_transcurrido = f"{int(minutos):02}:{int(segundos):02}"

        lista_pedidos = []
        for pedido in comanda.pedidos.all():
            tiempo_excedido = False
            tiempo_restante = "00:00"
            if pedido.hora_ini and pedido.producto.tiempo:
                delta = now() - pedido.hora_ini
                minutos_transcurridos = delta.total_seconds() // 60
                segundos_transcurridos = delta.total_seconds() % 60
                tiempo_restante = f"{int(minutos_transcurridos):02}:{int(segundos_transcurridos):02}"
                tiempo_excedido = minutos_transcurridos >= pedido.producto.tiempo.minute

            lista_pedidos.append({
                "id": pedido.id,
                "cantidad": pedido.cantidad,
                "producto": pedido.producto.nombre,
                "estado": pedido.estado,
                "notas": pedido.notas or "Sin notas",
                "hora_ini": pedido.hora_ini,
                "tiempo_estimado": pedido.producto.tiempo.minute if pedido.producto.tiempo else None,
                "tiempo_excedido": tiempo_excedido,
                "tiempo_transcurrido": tiempo_restante,
            })

        datos_comandas.append({
            "id": comanda.id,
            "mesa": comanda.mesa.numero_mesa if comanda.mesa else "Sin mesa",
            "notas": comanda.notas or "Sin notas",
            "total_pedidos": total_pedidos,
            "pedidos_preparados": pedidos_preparados,
            "tiempo_transcurrido": tiempo_transcurrido,
            "pedidos": lista_pedidos,
        })

    return render(request, 'preparacion/preparacion.html', {"comandas": datos_comandas})


@login_required
def actualizar_comandas(request):
    comandas = Comandas.objects.filter(pedidos__estado__in=[0, 3]).distinct().prefetch_related('pedidos__producto', 'pedidos__comensal')
    datos_comandas = []
    for comanda in comandas:
        pedidos = comanda.pedidos.filter(estado__in=[0, 3])  # Solo pedidos en preparación o marcados
        total_pedidos = pedidos.count()
        pedidos_preparados = pedidos.filter(estado=3).count()

        # Calcular tiempo transcurrido desde el primer pedido
        primer_pedido = pedidos.order_by('hora_ini').first()
        tiempo_transcurrido = "00:00"
        tiempo_inicio = None
        if primer_pedido and primer_pedido.hora_ini:
            tiempo_inicio = primer_pedido.hora_ini.isoformat()
            delta = now() - primer_pedido.hora_ini
            minutos = delta.total_seconds() // 60
            segundos = delta.total_seconds() % 60
            tiempo_transcurrido = f"{int(minutos):02}:{int(segundos):02}"

        lista_pedidos = []
        for pedido in pedidos:
            tiempo_excedido = False
            tiempo_restante = "00:00"
            if pedido.hora_ini and pedido.producto.tiempo:
                delta = now() - pedido.hora_ini
                minutos_transcurridos = delta.total_seconds() // 60
                segundos_transcurridos = delta.total_seconds() % 60
                tiempo_restante = f"{int(minutos_transcurridos):02}:{int(segundos_transcurridos):02}"
                tiempo_excedido = minutos_transcurridos >= pedido.producto.tiempo.minute

            lista_pedidos.append({
                "id": pedido.id,
                "cantidad": pedido.cantidad,
                "producto": pedido.producto.nombre,
                "estado": pedido.estado,
                "notas": pedido.notas or "Sin notas",
                "hora_ini": pedido.hora_ini.isoformat() if pedido.hora_ini else None,
                "tiempo_estimado": pedido.producto.tiempo.minute if pedido.producto.tiempo else None,
                "tiempo_excedido": tiempo_excedido,
                "tiempo_transcurrido": tiempo_restante,
            })

        if lista_pedidos:
            datos_comandas.append({
                "id": comanda.id,
                "mesa": comanda.mesa.numero_mesa if comanda.mesa else "Sin mesa",
                "notas": comanda.notas or "Sin notas",
                "total_pedidos": total_pedidos,
                "pedidos_preparados": pedidos_preparados,
                "tiempo_transcurrido": tiempo_transcurrido,
                "tiempo_inicio": tiempo_inicio,  # Incluye el tiempo de inicio de la comanda
                "pedidos": lista_pedidos,
            })
    return JsonResponse({"comandas": datos_comandas})




# Cambiar estado de un pedido
@csrf_exempt
@login_required
def actualizar_estado_pedido(request, pedido_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nuevo_estado = data.get("estado")
            if nuevo_estado is None:
                return JsonResponse({"error": "Estado no proporcionado."}, status=400)

            pedido = get_object_or_404(Pedidos, id=pedido_id)
            pedido.estado = nuevo_estado
            pedido.save()

            return JsonResponse({"success": True, "nuevo_estado": nuevo_estado})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)


# Cambiar estado de pedidos seleccionados a preparados
@csrf_exempt
@login_required
def marcar_comanda_preparada(request, comanda_id):
    if request.method == "POST":
        try:
            comanda = get_object_or_404(Comandas, id=comanda_id)
            # Filtrar pedidos seleccionados con estado "marcado" (3)
            pedidos_seleccionados = comanda.pedidos.filter(estado=3)
            
            if not pedidos_seleccionados.exists():
                return JsonResponse({"error": "No hay pedidos seleccionados."}, status=400)
            
            # Actualizar pedidos seleccionados a "preparado" (2) y registrar hora_fin
            pedidos_seleccionados.update(estado=2, hora_fin=now())
            
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)

#######################################################################################
# FIN Módulo de preparación para Cocina o barra
#######################################################################################

def comandas(request):
    comandas =  Comandas.objects.all().order_by("-id")
    actual =datetime.now()
    print(actual)
    data = {
        'comandas': comandas,
        'actual' : actual
        }
    
    if 'nuevocomansal' in request.POST:
        print("aquitoy")
        form = ComensalForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Agregado correctamente")
            return redirect(to="comandas")
        else:
            messages.warning(request, "No se pudo crear la comanda")
    else:
        form = ComensalForm() 

    return render(request,'comandas/comandas/comandas.html',data)

def listarcomandas(request, id):
    comandas =  Comandas.objects.filter(estado=id).order_by("-id")
    data = {
        'comandas': comandas
        }
    
    return render(request,'comandas/comandas/comandas.html',data)

def detallecomandas(request,id,det):
    pedidos = Pedidos.objects.filter(comanda_id = id, estado = det)
    productos = Producto.objects.all()
    pendientes = Pedidos.objects.filter(comanda_id = id,estado = 2).count()
    ids = id

    estado = {
            'estado': 1
        }
    
    if request.method == 'POST':
        idpedido = request.POST['idpedido']
        pedido = get_object_or_404(Pedidos, id=idpedido)
        form = updatepedidoForm(estado, instance=pedido)

        if form.is_valid():
            form.save()
            messages.success(request, "Pedido entregado")
           
       
    else: form = updatepedidoForm()
    data = {
        'pedidos' :pedidos,
        'ids': ids,
        'productos': productos,
        'pendientes': pendientes
    }

    return render(request, 'comandas/comandas/detallecomanda.html',data)

def agregarpedido(request, comanda,id):
    productos = Producto.objects.filter(categoria=id)
    categorias = Categorias.objects.all()
    comensales = Comensales.objects.filter(comanda=comanda)
    idcomanda = comanda
    pedidos = Pedidos.objects.filter(comanda=comanda,estado = 4).order_by('comensal') 
    vali = Pedidos.objects.filter(comanda=comanda,estado = 4).order_by('comensal').count()   
    print(vali)
    
    if 'todos' in request.POST:
        for pedido in pedidos:
            print(pedido.id)
            estado = {
                'estado': 0
            }
            updatePedido = get_object_or_404(Pedidos, id=pedido.id)
            form = updatepedidoForm(estado, instance=updatePedido)
            if form.is_valid():
                form.save()
                messages.success(request, "Pedidos enviados a cocina")

    if 'uno' in request.POST:

        precio = request.POST['precio']
        cantidad = request.POST['cantidad']
        total_pedido = int(precio)*int(cantidad)
       
        pedido ={
            'cantidad' : request.POST['cantidad'],
            'total_pedido' : total_pedido,
            'estado' : 4, 
            'comanda' : comanda,
            'comensal' : request.POST['comensal'],
            'producto' : request.POST['producto'],
            'notas' : request.POST['notas']  
        }
        form = agregarpedidoForm(pedido)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido agregado")
    else:
        form = agregarpedidoForm()
    data ={
        'idcomanda': idcomanda,
        'productos': productos,
        'categorias' : categorias,
        'comensales' : comensales,
        'pedidos' : pedidos,
        'vali':vali
    }

    return render(request, 'comandas/comandas/agregarpedido.html',data)

def nuevacomanda(request):
    
    mesas = Mesa.objects.all().order_by('numero_mesa').values()
    if request.method == 'POST':
        idmesa = request.POST['mesa']
        mesas2 = get_object_or_404(Mesa, id=idmesa)
     
        estado = {
            'estado': 1
        }

        form = ComandasForm(request.POST)  # Pasamos el usuario al formulario
        form2 = MesaupdateForm(estado, instance=mesas2)

        if form.is_valid():
            form.save()
            form2.save()  
            messages.success(request, "Comanda creada")
            return redirect('comandas')  # Redirige a la lista de comandas
        else:
            messages.warning(request, "No se pudo crear la comanda")
    else:
        form = ComandasForm()  
    
    data ={
        'mesas' : mesas,
        'form'  : ComandasForm()
    }
    return render(request, 'comandas/comandas/nuevacomanda.html',data )

def desglosecuenta(request,id):
    detallePedidos = Pedidos.objects.filter(comanda=id).values('comensal').annotate(total=Sum('total_pedido'))
    detallecomensa = Pedidos.objects.filter(comanda=id) 
    coniva = Pedidos.objects.filter(comanda=id).values('comensal').annotate(
    total=Func(
        (Sum('total_pedido')*1.19)
        , 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
    iva = Pedidos.objects.filter(comanda=id).values('comensal').annotate(
    total=Func(
        (Sum('total_pedido')*0.19), 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
    propinasola = Pedidos.objects.filter(comanda=id).values('comensal').annotate(
    total=Func(
        (Sum('total_pedido') * 1.19 * 0.10), 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
   
    propina = Pedidos.objects.filter(comanda=id).values('comensal').annotate(
    total=Func(
        (Sum('total_pedido') * 1.19 * 1.10), 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
    
    TotalDetallePedidos = Pedidos.objects.filter(comanda=id).aggregate(total=Sum('total_pedido'))
     
    TotalConiva = Pedidos.objects.filter(comanda=id).aggregate(
    total=Func(
        (Sum('total_pedido')*1.19)
        , 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
   
    TotalIva = Pedidos.objects.filter(comanda=id).aggregate(
    total=Func(
        (Sum('total_pedido')*0.19), 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
    TotalPropinasola = Pedidos.objects.filter(comanda=id).aggregate(
    total=Func(
        (Sum('total_pedido') * 1.19 * 0.10), 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
   
    TotalPropina = Pedidos.objects.filter(comanda=id).aggregate(
    total=Func(
        (Sum('total_pedido') * 1.19 * 1.10), 
        function='FLOOR',  # Cambia a ROUND si quieres redondear.
        output_field=IntegerField()
        )
    )
   
    comanda = Comandas.objects.filter(id=id).first()
    contadorPedidos = Pedidos.objects.filter(comanda=id).count()

    count=0
    for pedidos in detallecomensa:
            if pedidos.estado ==1:
                count =1+count
           
    
            if request.method == 'POST':
                    if contadorPedidos == count:
                        comanda = get_object_or_404(Comandas, id=id)
                        mesa = comanda.mesa.id
                        print(mesa)
                        medio_pago = request.POST['medio_pago']
                        mesas2 = get_object_or_404(Mesa, id=mesa)
                        
                    
                        estado1 = {
                            'estado': 0
                        }

                        estado = {
                            'fecha_fin':datetime.now(), 
                            'valor_neto': TotalDetallePedidos["total"], 
                            'iva': TotalIva["total"] , 
                            'sub_total': TotalConiva["total"], 
                            'propina': TotalPropinasola["total"], 
                            'total': TotalPropina["total"], 
                            'estado' : 1, 
                            'medio_pago' : medio_pago

                        }

                        form = cierrecomandaForm(estado, instance=comanda)  # Pasamos el usuario al formulario
                        form2 = MesaupdateForm(estado1, instance=mesas2)

                        if form.is_valid():
                            form.save()
                            form2.save()  
                            messages.success(request, "Comanda cerrada")
                            return redirect('comandas')  # Redirige a la lista de comandas
                        else:
                            messages.error(request, "No se pudo crear la comanda")
                    else:
                        messages.error(request, "Debe entregar todos los pedidos","error")
            else:
                form = ComandasForm() 
        
    

    data = {
        'detallePedidos' : detallePedidos,
        'detallecomensa' : detallecomensa,
        'coniva' : coniva,
        'iva' : iva,
        'propina' : propina,
        'id':id,
        'propinasola' :propinasola,
        'TotalDetallePedidos' : TotalDetallePedidos,
        'TotalConiva' : TotalConiva,
        'TotalIva' : TotalIva,
        'TotalPropinasola' :TotalPropinasola,
        'TotalPropina' : TotalPropina,
        'comanda' : comanda  
    }
    return  render(request,'comandas/comandas/desglosecuenta.html',data)

def eliminar_pedido(request, id,idcomanda):
    pedidos = get_object_or_404(Pedidos,id=id)
    pedidos.delete()
    messages.success(request, "Eliminado correctamente")
    return  redirect('agregarpedido', comanda= idcomanda, id=1)

def mismesas(request,id):
    mesas = Mesa.objects.filter(estado = id) 
    data = {
        'mesas': mesas
    }
    return render(request,'comandas/comandas/mismesas.html',data)

def solicitudes(request):
    solicitudes = Solicitudes.objects.all()
    print(solicitudes)
    print("aquu")
    data = {
        'solicitudes': solicitudes
    }
    
    return render(request,'comandas/base.html',data)