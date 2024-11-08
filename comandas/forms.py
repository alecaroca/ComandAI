from django import forms
from .models import User,Producto,Categorias,Mesa
from django.contrib.auth.forms import UserCreationForm


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

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