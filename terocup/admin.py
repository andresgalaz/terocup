from django import forms
from django.contrib import admin

from datetime import datetime
from dateutil.relativedelta import relativedelta

from terocup.models import Paciente, Consultorio, Programa, Sexo, Diagnotico
import terocup.rut as rut

from django.conf.locale.es import formats as es_formats

es_formats.DATETIME_FORMAT = "d M Y H:i:s"


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

    def clean_rut(self):
        cRut = self.cleaned_data['rut']
        if not rut.valida(cRut):
            raise forms.ValidationError('Rut no válido')
        return None if cRut is None else cRut.upper()


class PacienteAdmin(admin.ModelAdmin):
    form = PacienteForm
    readonly_fields = ('edad',)

    def edad(self, obj):
        edad = relativedelta(datetime.now(), obj.fechaNacimiento)
        return edad.years


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Consultorio)
admin.site.register(Diagnotico)
admin.site.register(Programa)
admin.site.register(Sexo)
