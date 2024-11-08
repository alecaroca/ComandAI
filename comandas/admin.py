from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from comandas.models import User
from .models import Categorias, Producto

@admin.register(User) 
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(Categorias)
admin.site.register(Producto)
#admin.site.register(mesa)
# Register your models here.
