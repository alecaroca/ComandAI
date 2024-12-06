from rest_framework.permissions import BasePermission, IsAuthenticated
from comandas.models import Comensales

class IsComensalApp(BasePermission):
    """
    Permite el acceso solo a solicitudes que incluyan un token válido en los headers.
    """
    def has_permission(self, request, view):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return False

        # Verificar si el token pertenece a un comensal válido
        return Comensales.objects.filter(token=token).exists()


class IsAllowedIP(BasePermission):
    """
    Permite el acceso solo si la solicitud proviene de una IP permitida.
    """
    ALLOWED_IPS = ["127.0.0.1", "::1"]  # Lista de IPs permitidas

    def has_permission(self, request, view):
        ip = self.get_client_ip(request)
        return ip in self.ALLOWED_IPS

    def get_client_ip(self, request):
        # Extrae la IP del header de la solicitud
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
