from proyectos.models import Objetivo
from cuentas.models import Estudiante
from inicio.models import Registro
from django.db import models



# Create your models here.

class Tarea(Registro):
    nombre = models.CharField(max_length=500)
    estudiante = models.ManyToManyField(Estudiante)
    tareaSuperior = models.ForeignKey('self', on_delete=models.SET_NULL,null=True,blank=True)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.SET_NULL,null=True)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


class AsignacionesEnviadas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.SET_NULL,null=True)
    tarea = models.ForeignKey(Tarea, on_delete=models.SET_NULL,null=True)

