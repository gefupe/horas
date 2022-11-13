from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cuentas.models import *
from horas.forms import EstudiantesForm
from actividades.models import Actividad
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/cuentas/ingreso/')
def estudiantes(request):
    '''Recopila la información de todos los estudiantes
    registrados para mostrarla en una lista.
    '''
    staffBotonVistaEstudiante = False

    if request.method == "POST":
        list_of_inputs = request.POST.getlist('inputs')
        if request.POST.get('studentButton'):
            studentButtonItemValue = request.POST.getlist('studentButton')
            estudianteAVer = Estudiante.objects.filter(
                id=studentButtonItemValue[0])
            staffBotonVistaEstudiante = True
            response = HttpResponseRedirect("/")
            response.headers["estudiante"] = estudianteAVer[0].id
            user = estudianteAVer[0].user
            return response
            # return render (request=request, template_name="../../inicio/templates/index.html", context={"estudianteID":estudianteAVer[0].id,})

    estudiantes_list = Estudiante.objects.all().filter(user__is_staff=False)
    
    actividades_list = Actividad.objects.all()

    horasEstudianteslist = []
    porcentajeEstudianteslist = []
    porcentajeWidthEstudianteslist = []

    horasTotalesPorEstudiante = 0
    for estudiante in estudiantes_list:

        horasTotalesPorEstudiante = 0
        for actividad in actividades_list:

            if actividad.estudiante.user.username == estudiante.user.username:
                if actividad.estado == "A":
                    horasTotalesPorEstudiante += actividad.horas

        horasEstudianteslist.append(horasTotalesPorEstudiante)
        porcentaje = round((100 / 300) * horasTotalesPorEstudiante)
        porcentajeEstudianteslist.append(porcentaje)
        porcentajeWidthEstudianteslist.append(int(porcentaje))

    zipHoras = zip(estudiantes_list, horasEstudianteslist,
                   porcentajeEstudianteslist, porcentajeWidthEstudianteslist)

    context = {
        "zipHoras": zipHoras,
        "horaslist": horasEstudianteslist,
        "estudiantes": estudiantes_list,
        "actividades": actividades_list,
        "porcentajeList": porcentajeEstudianteslist,
        "porcentajeWidthList": porcentajeWidthEstudianteslist
    }

    return render(request, "estudiantes.html", context)


@login_required(login_url='/cuentas/ingreso/')
def editar_estudiante(request, id):

    estudiante = get_object_or_404(Estudiante, id=id)

    form = EstudiantesForm(request.POST or None, instance=estudiante)
    form.fields['user'].widget = forms.HiddenInput()
    form.fields['carrera'].widget = forms.HiddenInput()
    form.fields['fecha_inicio'].widget = forms.HiddenInput()
    form.fields['fecha_final'].widget = forms.HiddenInput()

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/estudiantes")

    # Acción: editar
    crear = False

    # Contexto
    context = {
        "crear": crear,
        "estudiante_form": form,
        "estudiante": estudiante,
    }

    return render(request, "editar_estudiante.html", context)


@login_required(login_url='/cuentas/ingreso/')
def equipos(request):
    '''Lista de equipos de estudiantes.

    Incluye información el nombre y descripción.
    '''
    context = {
        'saludo': 'hola',
    }
    return render(request, 'equipos.html', context)