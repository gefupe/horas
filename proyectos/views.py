from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import AreasForm, FiltrosProyectoForm, ProyectosForm
from proyectos.models import Proyecto
from proyectos.models import Area
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
import time

# Create your views here.

'''Menú de funciones

- Lista de proyectos (def proyectos --> proyectos.html)
- Crear proyecto (def crear_proyecto --> crear_proyecto.html)
- Editar proyecto (def editar_proyecto --> crear_proyecto.html, con datos)

- Crear objetivo (def crear_objetivo --> crear_objetivo.html)
- Editar objetivo (def crear_objetivo --> crear_objetivo.html, con datos)

'''


@login_required(login_url='/cuentas/ingreso/')
def proyectos(request):
    '''Recopila todos los proyectos para desplegarlos
    en una tabla con la lista de proyectos que no
    están en papelera. Además, crea un formulario 
    para filtrar los proyectos según categorías.
    '''

    # Obtiene la lista de proyectos
    proyectos = Proyecto.objects.all()

    # Formulario para los filtros
    if request.method == "POST":
        
        # Crea el filtro para la tabla
        form = FiltrosProyectoForm(request.POST or None)

        if form.is_valid():
            if form.cleaned_data.get('nombre'):
                proyectos = proyectos.filter(
                    nombre__contains=form.cleaned_data.get('nombre'))
            if form.cleaned_data.get('descripcion'):
                proyectos = proyectos.filter(
                    descripcion__contains=form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('profesor'):
                proyectos = proyectos.filter(
                    profesor=form.cleaned_data.get('profesor'))
            if form.cleaned_data.get('area'):
                proyectos = proyectos.filter(
                    area=form.cleaned_data.get('area'))
            if form.cleaned_data.get('ubicacion'):
                proyectos = proyectos.filter(
                    ubicacion__contains=form.cleaned_data.get('ubicacion'))

        # Crea el botón de enviar a papelera
        if request.POST.get('deleteButton'):
            deleteButtonItemValue = request.POST.getlist('deleteButton')
            obj = Proyecto(id=deleteButtonItemValue[0])
            Proyecto.objects.filter(
                id=deleteButtonItemValue[0]).update(enPapelera='True')

        # return HttpResponseRedirect("/proyectos")

    form = FiltrosProyectoForm()

    context = {
        "proyectos": proyectos,
        "filtros_form": form
    }

    return render(request, "proyectos.html", context)


@ login_required(login_url='/cuentas/ingreso/')
def crear_proyecto(request):
    '''Crea formulario para recopilar los datos
    de un nuevo proyecto.
    '''

    # Crea formulario con todos los campos de información del proyecto
    if request.method == "POST":
        form = ProyectosForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/proyectos")

    form = ProyectosForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # Quita del formulario las áreas borradas
    areas_noborrados = Area.objects.all()
    areas_noborrados = areas_noborrados.filter(enPapelera=False)
    form.fields["area"].queryset = areas_noborrados

    # Crear o editar
    crear = True

    context = {
        "crear": crear,
        "proyecto_form": form
    }

    return render(request, "crear_proyecto.html", context)


@ login_required(login_url='/cuentas/ingreso/')
def editar_proyecto(request, id):
    '''Carga un formulario con los datos de un 
    proyecto ya registrado para edición.
    '''

    # Recupera la información del proyecto seleccionado
    obj = get_object_or_404(Proyecto, id=id)

    # Carga el formulario con la instancia del proyecto
    form = ProyectosForm(request.POST or None, instance=obj)
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # Quita del formulario las áreas borradas
    areas_noborrados = Area.objects.all()
    areas_noborrados = areas_noborrados.filter(enPapelera=False)
    form.fields["area"].queryset = areas_noborrados

    # Valida el formulario y lo guarda
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/proyectos")

    # Crear o editar
    crear = False

    context = {
        "crear": crear, 
        "proyecto_form": form
    }

    return render(request, "crear_proyecto.html", context)


@ login_required(login_url='/cuentas/ingreso/')
def crear_area(request):

    if request.method == "POST":
        form = AreasForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)  # para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/proyectos")

    form = AreasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    return render(request=request, template_name="../templates/crear_area.html", context={"area_form": form})


def proyectosInfo(request):
    listaProyectos = Proyecto.objects.all()

    return render(request=request,  template_name="../templates/proyectosInfo.html", context={"listaProyectos": listaProyectos})


def proyecto(request, id):
    proyecto = Proyecto.objects.filter(id=id)
    proyectoHoras = 1
    objetivos = proyecto[0].objetivo_set.filter(enPapelera=False)

    listatareas = []
    for objetivo in objetivos:
        tareas = objetivo.tarea_set.filter(enPapelera=False)
        for tarea in tareas:
            listatareas.append(tarea.nombre)

    return render(request, "proyecto.html", context={"proyecto": proyecto[0],
                                                     "proyectoHoras": proyectoHoras, "objetivos": objetivos, "tareas": listatareas})
