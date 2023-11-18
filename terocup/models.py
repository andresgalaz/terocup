from django.db import models


class Sexo(models.Model):
    sexo = models.CharField(max_length=10)

    def __str__(self):
        return self.sexo


class Programa(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class Consultorio(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombre = models.CharField(max_length=120)
    sexo = models.ForeignKey( Sexo, on_delete=models.CASCADE, related_name="paciente_sexo")
    programa = models.ForeignKey( Programa, on_delete=models.CASCADE, related_name="paciente_programa")
    consultorio = models.ForeignKey( Consultorio, on_delete=models.CASCADE, related_name="paciente_consultorio")

    def __str__(self):
        return self.nombre
