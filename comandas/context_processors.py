from comensal.models import Solicitudes
#from comandas.forms import updateSolicitudForm
#from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib import messages

def solicitudes(request):

    solicitudes = Solicitudes.objects.all()
    data = {
        'solicitudes': solicitudes
    }
    return (data)

"""     if 'solicitud' in request.POST:
        id = request.POST['id']
        idsol = get_object_or_404(Solicitudes, id=id)
        estado_solicutud = request.POST['estado']
   
   
        form2 = updateSolicitudForm(estado_solicutud, instance=idsol)

        if form2.is_valid():
            form2.save()  
            messages.success(request, "Comanda creada")
        
        else:
            messages.warning(request, "No se pudo crear la comanda")
    else:
        form = updateSolicitudForm()   """

 
   