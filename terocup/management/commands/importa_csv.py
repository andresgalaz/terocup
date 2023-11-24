# -*- coding: utf-8 -*-
__author__ = "Andrés Galaz"
__license__ = "LGPL"
__email__ = "andres.galaz@gmail.com"
__version__ = "v1.0"

import csv
import re
# import uuid
from datetime import datetime
from django.core.management import BaseCommand
from django.utils import timezone
from django.db.utils import DataError
from django.db import transaction
from terocup.models import Comuna, Diagnostico, ObsAdicional, Pais, Paciente, Prevision, Programa, Sexo
import terocup.util_rut as util_rut


def str2date(cFecha):
    try:
        cFecha = cFecha.replace(".", "-").replace("/", "-")
        if re.search(
                "^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])" +
                "(\\.|-|/)([1-9]|0[1-9]|1[0-2])(\\.|-|/)" +
                "([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$",
                cFecha):
            return datetime.strptime(cFecha, '%d-%m-%Y').date()
        elif re.search(
                "^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])" +
                "(\\.|-|/)([1-9]|0[1-9]|1[0-2])(\\.|-|/)" +
                "([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$",
                cFecha):
            return datetime.strptime(cFecha, '%Y-%m-%d').date()
    except Exception:
        pass


def str2boolean(cBol):
    cBol = cBol.strip().upper()
    if cBol == 'S' or cBol == 'SI' or cBol == 'T' or cBol == 'TRUE' or cBol == '1':
        return True
    if cBol == 'N' or cBol == 'NO' or cBol == 'F' or cBol == 'FALSE' or cBol == '0':
        return False
    return None


def str2number(cNum):
    cNum = cNum.strip().replace(".", "").replace("\xa0%", "")
    try:
        if cNum.find(',') >= 0:
            cNum = cNum.replace(",", ".")
            return float(cNum)
        return int(cNum)
    except Exception:
        return None


def isRowEmpty(row):
    for r in row:
        if r.strip() != '':
            return False
    return True


class Command(BaseCommand):
    help = "Carga datos desde un archivo CSV."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]

        # encoding = 'cp437'
        with open(file_path, "r", encoding='utf8') as csv_file:
            data = list(csv.reader(csv_file, delimiter=";"))
            # Valida. Si hay errores no procesa nada
            nLinea = 1
            nError = 0
            for row in data:  # data[1:]:
                nLinea += 1
                if isRowEmpty(row):
                    continue

                # 0 mes/año de derivacion;
                csvRut = row[0].strip()
                csvCP = row[1].strip()
                csvNFicha = row[2].strip()
                csvPrimerApellido = row[3].strip()
                csvSegundoApellido = row[4].strip()
                csvNombre = row[5].strip()
                csvFecNac = row[6].strip()
                # Edad col 7
                csvPrevision = row[8].strip().upper()
                csvSexo = row[9].strip().upper()
                csvNacionalidad = row[10].strip().upper()
                csvComuna = row[11].strip().upper()
                csvPrograma = row[12].strip().upper()
                csvDiagnostico = row[13].strip().upper()
                csvSename = row[14].strip()
                csvMigrante = row[15].strip()
                csvPuebloOriginario = row[16].strip()
                csvObservacion = row[17].strip()
                csvObsAdicional = row[18].strip()
                # ============================

                if util_rut.valida(csvRut):
                    rut = util_rut.formatoCorto(csvRut)
                else:
                    nError += 1
                    print(nLinea, "Error rut:"+csvRut)

                CP = csvCP
                numeroFicha = csvNFicha
                fechaNacimiento = str2date(csvFecNac)

                if csvPrimerApellido == '' or csvNombre == '':
                    nError += 1
                    print(nLinea, "Falta nomre o apellido:"+csvNombre+","+csvPrimerApellido)

                primerApellido = csvPrimerApellido
                segundoApellido = csvSegundoApellido
                nombre = csvNombre

                prevision = None
                try:
                    if csvPrevision == '':
                        nError += 1
                        print(nLinea, "Falta prevision")
                    else:
                        prevision = Prevision.objects.all().get(nombre=csvPrevision)
                except Exception:
                    pass

                sexo = None
                try:
                    if csvSexo == '':
                        nError += 1
                        print(nLinea, "Falta sexo")
                    else:
                        sexo = Sexo.objects.all().get(sexo=csvSexo)
                except Exception:
                    pass

                nacionalidad = None
                try:
                    if csvNacionalidad == '':
                        nError += 1
                        print(nLinea, "Falta Nacionalidad")
                    else:
                        nacionalidad = Pais.objects.all().get(nombre=csvNacionalidad)
                except Exception:
                    pass

                comuna = None
                try:
                    if csvComuna == '':
                        nError += 1
                        print(nLinea, "Falta Comuna")
                    else:
                        comuna = Comuna.objects.all().get(nombre=csvComuna)
                except Exception:
                    pass

                programa = None
                try:
                    if csvPrograma != '':
                        programa = Comuna.objects.all().get(nombre=csvPrograma)
                except Exception:
                    pass

                diagnostico = None
                try:
                    if csvDiagnostico != '':
                        diagnostico = Diagnostico.objects.all().get(nombre=csvDiagnostico)
                except Exception:
                    pass

                sename = str2boolean(csvSename)
                migrante = str2boolean(csvMigrante)
                puebloOriginario = str2boolean(csvPuebloOriginario)
                observacion = csvObservacion
                obsAdicional = csvObsAdicional

                if nError > 0:
                    continue

                with transaction.atomic():
                    try:
                        if prevision is None:
                            prevision = Prevision.objects.create(nombre=csvPrevision)

                        if sexo is None:
                            sexo = Sexo.objects.create(sexo=csvSexo)

                        if nacionalidad is None:
                            nacionalidad = Pais.objects.create(nombre=csvNacionalidad)

                        if comuna is None:
                            comuna = Comuna.objects.create(nombre=csvComuna)

                        if programa is None and csvPrograma != '':
                            programa = Programa.objects.create(nombre=csvPrograma)

                        if diagnostico is None and csvDiagnostico != '':
                            diagnostico = Diagnostico.objects.create(nombre=csvDiagnostico)

                        try:
                            paciente = Paciente.objects.all().get(rut=rut)
                            print(paciente)
                        except Exception as e:
                            print(e)
                            paciente = Paciente.objects.create(
                                rut=rut,
                                cp=CP,
                                numero_ficha=numeroFicha,
                                primer_apellido=primerApellido,
                                segundo_apellido=segundoApellido,
                                nombre=nombre,
                                fecha_nacimiento=fechaNacimiento,
                                prevision=prevision,
                                sexo=sexo,
                                nacionalidad=nacionalidad,
                                comuna=comuna,
                                programa=programa,
                                diagnostico=diagnostico,
                                sename=sename,
                                migrante=migrante,
                                pueblo_originario=puebloOriginario,
                                observacion=observacion
                            )
                        print(paciente)

                        if obsAdicional != '':
                            ObsAdicional.objects.create(paciente=paciente, texto=obsAdicional)

                    except DataError as e:
                        transaction.set_rollback(True)
                        print(nLinea, 'Error SQL:', e, row)
                        exit(-1)

        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(f"""
========================================================================
La carga CSV tomó: {(end_time-start_time).total_seconds()} segundos.
Lineas procesadas {nLinea}
Errores encontrados {nError}
========================================================================
"""))
