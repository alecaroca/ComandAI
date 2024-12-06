# Vista para gestionar solicitudes de acceso de comensales
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from comandas.models import Mesa, Comandas, Comensales, Pedidos
from .models import Solicitudes
from django.shortcuts import render, redirect
import uuid
import requests
from django.conf import settings

#########################################################################
# Vista para mostrar el formulario de ingreso del comensal
#########################################################################
def ingreso_comensal(request):
    """
    Muestra un formulario con el número de mesa prellenado o redirige al menú si ya tiene un token válido.
    """
    # Verificar si la cookie 'comensalToken' está presente
    token = request.COOKIES.get('comensalToken')
    if token:
        # Verificar si el token corresponde a un comensal válido
        if Comensales.objects.filter(token=token).exists():
            return redirect('/comensal/menu/')

    # Mostrar el formulario si no hay token válido
    numero_mesa = request.GET.get('mesa', None)
    if not numero_mesa:
        return render(request, 'error.html', {'mensaje': 'Número de mesa no especificado.'})
    return render(request, 'ingreso.html', {'numero_mesa': numero_mesa})


#########################################################################
# Vista para mostrar el formulario de ingreso del comensal
#########################################################################
@method_decorator(csrf_exempt, name='dispatch')
class RegistrarComensalView(View):
    """
    Vista para registrar una nueva solicitud de comensal.
    Verifica que no exista una solicitud pendiente y crea una nueva solicitud.
    """
    def post(self, request, *args, **kwargs):
   
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        numero_mesa = request.POST.get('mesa', '').strip()

        # Validar que el nombre es obligatorio
        if not nombre:
            return JsonResponse({'success': False, 'message': 'El nombre es obligatorio.'}, status=400)

        # Validar que el número de mesa es obligatorio
        if not numero_mesa:
            return JsonResponse({'success': False, 'message': 'El número de mesa es obligatorio.'}, status=400)

        # Validar que la mesa exista
        try:
            mesa = Mesa.objects.get(numero_mesa=numero_mesa)
  
        except Mesa.DoesNotExist:
  
            return JsonResponse({'success': False, 'message': f'La mesa {numero_mesa} no existe.'}, status=404)

        # Verificar si ya hay una solicitud pendiente para la mesa
        solicitudes_pendientes = Solicitudes.objects.filter(mesa=mesa, estado=0)

        if solicitudes_pendientes.exists():
    
            return JsonResponse({
                'success': True,
                'message': 'Otra solicitud está en proceso. Esperando aprobación.',
                'solicitud_id': solicitudes_pendientes.first().id
            })

        # Crear una nueva solicitud en estado pendiente
        solicitud = Solicitudes.objects.create(
            tipo='comensal',
            estado=0,
            mesa=mesa,
            nombre=nombre,
            correo=correo,
            telefono=telefono
        )
     

        return JsonResponse({
            'success': True,
            'message': 'Solicitud registrada. Esperando aprobación.',
            'solicitud_id': solicitud.id
        })



#########################################################################
# Vista para mostrar el formulario de ingreso del comensal
#########################################################################
class ConsultarEstadoSolicitudView(View):
    """
    Vista para consultar el estado de una solicitud específica.
    Responde con el estado actual de la solicitud.
    """
    def get(self, request, solicitud_id, *args, **kwargs):

        try:
            solicitud = Solicitudes.objects.get(id=solicitud_id)
            mesa = solicitud.mesa

            # Verificar si la solicitud fue aprobada
            if solicitud.estado == 1:
                comanda, creada = Comandas.objects.get_or_create(
                    mesa=mesa, estado=0, defaults={"mesero": mesa.mesero}
                )

                # Crear el comensal asociado a la comanda
                token = str(uuid.uuid4())

                Comensales.objects.create(
                    nombre=solicitud.nombre,  # Usar datos almacenados en la solicitud
                    correo=solicitud.correo,
                    telefono=solicitud.telefono,
                    comanda=comanda,
                    token=token
                )

                # Responder con éxito y redirigir al menú
                response = JsonResponse({'success': True, 'estado': 1, 'redirect_url': '/comensal/menu/'})
                response.set_cookie('comensalToken', token, httponly=True, max_age=3600 * 12)
                return response

            # Si la solicitud fue rechazada
            elif solicitud.estado == 2:
                return JsonResponse({'success': True, 'estado': 2, 'message': 'Solicitud rechazada. Intente nuevamente.'})

            # Si la solicitud aún está pendiente
            return JsonResponse({'success': True, 'estado': 0, 'message': 'Esperando aprobación del mesero.'})

        except Solicitudes.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Solicitud no encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error inesperado al consultar la solicitud.'}, status=500)

#########################################################################
# Vista para mostrar el menú al comensal
#########################################################################
from django.http import JsonResponse
from django.shortcuts import render
from comandas.models import Comensales
from django.conf import settings
import requests
import json

def menu_comensal(request):
    """
    Muestra el menú principal con categorías y productos.
    Incluye la barra superior con el nombre del comensal extraído del token.
    """
    # Leer el token del comensal desde la cookie
    comensal_token = request.COOKIES.get("comensalToken")
    if not comensal_token:
        return JsonResponse({'error': 'Token no encontrado. Inicie sesión nuevamente.'}, status=403)

    headers = {"Authorization": f"Bearer {comensal_token}"}
    API_BASE_URL = f"{settings.API_BASE_URL}"

    try:
        # Obtener categorías
        categorias_response = requests.get(f"{API_BASE_URL}categorias/", headers=headers)
        if categorias_response.status_code != 200:
            print(f"Error al obtener categorías: {categorias_response.text}")
            return JsonResponse({'error': 'Error al obtener las categorías'}, status=500)

        categorias = categorias_response.json()

        # Verificar si hay categorías
        if categorias:
            primera_categoria_id = categorias[0]['id']
            productos_response = requests.get(f"{API_BASE_URL}productos/?categoria={primera_categoria_id}", headers=headers)
            productos = productos_response.json() if productos_response.status_code == 200 else []
        else:
            primera_categoria_id = None
            productos = []

        # Obtener nombre del comensal y comanda
        comensal_nombre = None
        comanda_id = None
        try:
            comensal = Comensales.objects.get(token=comensal_token)
            comensal_nombre = comensal.nombre
            comanda_id = comensal.comanda.id  
        except Comensales.DoesNotExist:
            comensal_nombre = "Invitado"
        except AttributeError:
            print("El comensal no tiene una comanda asociada.")
            comanda_id = None

        # Enviar datos al template
        return render(request, "menuComensal.html", {
            "categorias": categorias,
            "productos": productos,
            "comensal_nombre": comensal_nombre,
            "comensal_token": comensal_token,
            "comanda_id": comanda_id, 
            "comensal_id": comensal.id
        })

    except requests.exceptions.RequestException as e:
        print("Error al conectar con la API:", e)
        return JsonResponse({'error': 'Error de conexión con la API'}, status=500)
    except Exception as e:
        print("Error interno al cargar el menú:", e)
        return JsonResponse({'error': 'Error interno al cargar el menú'}, status=500)

def confirmar_pedido(request):
    """
    Vista para la página de confirmar pedido.
    """
    try:
        # Obtener el token del comensal
        comensal_token = request.COOKIES.get("comensalToken")
        if not comensal_token:
            return JsonResponse({'error': 'Token del comensal no encontrado. Inicia sesión nuevamente.'}, status=403)

        # Verificar la existencia del comensal y obtener su comanda
        comensal = Comensales.objects.get(token=comensal_token)
        comensal_nombre = comensal.nombre
        comanda = comensal.comanda.id
      
        if not comanda:
            return JsonResponse({'error': 'No se encontró una comanda activa.'}, status=404)

        # Calcular la cantidad de pedidos en estado "confirmar"
        pedidos_cantidad = Pedidos.objects.filter(comanda=comanda, estado=4).count()

        # Renderizar el template con los datos necesarios
        return render(request, "confirmarPedidoComensal.html", {
            "comanda_id": comanda,  # Ahora se pasa directamente
            "comensal_token": comensal_token,
            "comensal_nombre": comensal_nombre,
            "pedidos_cantidad": pedidos_cantidad,
        })
    except Comensales.DoesNotExist:
        return JsonResponse({'error': 'Comensal no encontrado. Inicia sesión nuevamente.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)


def pedidos_comensal(request):
    token = request.COOKIES.get("comensalToken")

    try:
        comensal = Comensales.objects.get(token=token)
    except Comensales.DoesNotExist:
        return redirect("error_acceso")  # Redirige a la página de error

    context = {
        "comanda_id": comensal.comanda.id,
        "comensal_token": token,
        "comensal_nombre": comensal.nombre,
    }
    return render(request, "pedidosComensal.html", context)


def error_acceso(request):
    return render(request, 'errorAcceso.html', {'mensaje': 'Acceso no autorizado.'})

def solicitar_atencion(request):
    """Vista para que el usuario solicite atención"""

    
    return render(request, 'solicitarAtencionComensal.html')