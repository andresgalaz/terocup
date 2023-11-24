from django import forms
from django.contrib import admin

from datetime import datetime
from dateutil.relativedelta import relativedelta

from terocup.models import Comuna, Diagnostico, ObsAdicional, Paciente, Pais, Prevision, Programa, Sexo
import terocup.util_rut as util_rut

from django.conf.locale.es import formats as es_formats

es_formats.DATETIME_FORMAT = "d M Y H:i:s"


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

    def clean_rut(self):
        cRut = self.cleaned_data['rut']
        if not util_rut.valida(cRut):
            raise forms.ValidationError('Rut no válido')
        return None if cRut is None else cRut.upper()


class ObsAdicionalInline(admin.TabularInline):
    model = ObsAdicional


class PacienteAdmin(admin.ModelAdmin):
    form = PacienteForm
    list_display = ('rut', 'primer_apellido', 'segundo_apellido', 'nombre')
    search_fields = ('rut', 'primer_apellido', 'segundo_apellido', 'nombre')
    list_filter = ('programa', 'comuna')
    inlines = [ObsAdicionalInline,]

    readonly_fields = ('edad',)

    def edad(self, obj):
        edad = relativedelta(datetime.now(), obj.fechaNacimiento)
        return edad.years


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Comuna)
admin.site.register(Diagnostico)
admin.site.register(Pais)
admin.site.register(Prevision)
admin.site.register(Programa)
admin.site.register(Sexo)
