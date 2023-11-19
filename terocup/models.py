from django.db import models


class Consultorio(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class Diagnotico(models.Model):
    descripcion = models.CharField(max_length=120)

    def __str__(self):
        return self.descripcion


class Programa(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class Sexo(models.Model):
    sexo = models.CharField(max_length=10)

    def __str__(self):
        return self.sexo


class Paciente(models.Model):
    nombre = models.CharField(max_length=120)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, related_name="paciente_sexo")
    rut = models.CharField(max_length=10, null=True, blank=True)
    fechaNacimiento = models.DateField(auto_now_add=False, null=True, blank=True)
    numeroFicha = models.CharField(max_length=20, null=True, blank=True)
    programa = models.ForeignKey(Programa, models.SET_NULL, blank=True, null=True, related_name="paciente_programa")
    consultorio = models.ForeignKey(Consultorio, models.SET_NULL, blank=True, null=True, related_name="paciente_consultorio")
    diagnotico = models.ForeignKey(Diagnotico, models.SET_NULL, blank=True, null=True, related_name="paciente_diagnotico")

    def __str__(self):
        return self.nombre
