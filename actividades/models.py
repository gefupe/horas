from django.contrib.auth.models import User
from proyectos.models import Proyecto
from tareas.models import Tarea
from cuentas.models import Estudiante
from django.db import models
from django.conf import settings


# Create your models here.

class Actividad(models.Model):
    ESTADOS = (
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
        ('P', 'En Revisión'),
    )
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL,null=True)
    tarea = models.ForeignKey(Tarea, on_delete=models.SET_NULL,null=True)
    descripcion = models.CharField(max_length=500)
    fecha = models.DateField()
    horas = models.IntegerField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default= "En Revisión")
    enPapelera = models.BooleanField(default='False')
    fechaPapelera = models.DateField( blank=True,null=True)
    fechaCreacion = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.descripcion

