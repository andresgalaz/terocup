from django.contrib import admin

from terocup.models import Paciente, Consultorio, Programa

admin.site.register(Paciente)
admin.site.register(Consultorio)
admin.site.register(Programa)

