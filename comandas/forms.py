from django import forms
from .models import User,Producto,Categorias,Mesa, Comandas,Comensales, Pedidos
from django.contrib.auth.forms import UserCreationForm
from comensal.models import Solicitudes



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'tiempo': forms.TimeInput(attrs={'type': 'time'})
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "is_staff", "is_active", "groups" ]

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = '__all__'

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = '__all__'

class ComandasForm(forms.ModelForm):
    class Meta:
        model = Comandas
        fields = ["mesero","estado","mesa"]

class MesaupdateForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ["estado"]

class ComensalForm(forms.ModelForm):
    class Meta:
        model = Comensales
        fields = ["comanda","nombre"]
        
class agregarpedidoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ["cantidad","total_pedido","estado","comanda","comensal","producto","notas"] 

class updatepedidoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['estado']

class cierrecomandaForm(forms.ModelForm):
    class Meta:
        model = Comandas
        fields =['fecha_fin', 'valor_neto', 'iva', 'sub_total', 'propina', 'total', 'estado', 'medio_pago']

class updateSolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitudes
        fields = ['estado']