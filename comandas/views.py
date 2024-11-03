from comandas.api.serializers import UserSerializer
from urllib import request, response
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import User, Producto, Categorias, Mesa
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from .forms import ProductoForm, CustomUserCreationForm, CategoriasForm, MesaForm
from django.contrib import messages


def login(request):
    return render(request,'registration/login.html')
    
@login_required
def usuarios(request):
    usuarios = User.objects.all()
    data = {
        'usuarios': usuarios
    }
    print(usuarios[1]) 
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
