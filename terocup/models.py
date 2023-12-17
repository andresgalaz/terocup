from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

import terocup.util_rut as util_rut


class Comuna(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Diagnostico(models.Model):
    descripcion = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.descripcion


class Pais(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Prevision(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Programa(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Sexo(models.Model):
    sexo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.sexo


class Paciente(models.Model):
    rut = models.CharField(max_length=20, unique=True)
    cp = models.CharField(max_length=20)
    numero_ficha = models.CharField(max_length=120, null=True, blank=True)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(auto_now_add=False)
    prevision = models.ForeignKey(Prevision, models.SET_NULL, blank=True, null=True, related_name="paciente_prevision")
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, related_name="paciente_sexo")
    nacionalidad = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="paciente_nacionalidad")
    comuna = models.ForeignKey(Comuna, models.SET_NULL, blank=True, null=True, related_name="paciente_comuna")
    programa = models.ForeignKey(Programa, models.SET_NULL, blank=True, null=True, related_name="paciente_programa")
    diagnostico = models.ForeignKey(Diagnostico, models.SET_NULL, blank=True, null=True, related_name="paciente_diagnostico")
    sename = models.BooleanField(default=False, null=True)
    migrante = models.BooleanField(default=False, null=True)
    pueblo_originario = models.BooleanField(default=False, null=True)
    observacion = models.TextField(blank=True, null=True)

    @property
    def edad(self):
        "Retorna la edad del apciente."
        edad = relativedelta(datetime.now(), self.fecha_nacimiento)
        return edad.years

    def __str__(self):
        return self.nombre + ' ' + self.primer_apellido + ' ' + self.segundo_apellido

    def clean(self):
        if util_rut.valida(self.rut):
            self.rut = util_rut.formatoCorto(self.rut)
        else:
            raise ValidationError("RUT no es válido")


class ObsAdicional(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    texto = models.TextField()

    def __str__(self):
        return str(self.paciente.id)+'-'+str(self.id)
