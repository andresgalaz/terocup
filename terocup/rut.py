#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Andrés Galaz"
__license__ = "LGPL"
__email__ = "andres.galaz@gmail.com"
__version__ = "v1.0"


def calcDv(nRut):
    # Solo recibe la parte del RUT numérica
    rut = []
    for n in nRut:
        rut.append(n)
    rut.reverse()
    recorrido = 2
    multiplicar = 0
    digito = ""
    for x in rut:
        multiplicar += int(x) * recorrido
        if recorrido == 7:
            recorrido = 1
        recorrido += 1
        modulo = multiplicar % 11
        resultado = 11 - modulo
        if resultado == 11:
            digito = 0
        elif resultado == 10:
            digito = "K"
        else:
            digito = resultado
    return str(digito)


def limpia(cRut):
    # Elimina puntos y guiones
    return cRut.replace(".", "").replace("-", "").upper()


def formato(cRut):
    # Agrega separador de miles, guión y cero a la izquierda
    cRut = limpia(cRut)
    dv = cRut[-1]
    # Ajusta el nro rut a 8 largo máximo, si es menor que 8 llena con ceros a la iaquierda
    cRut = cRut[0: min(8, len(cRut) - 1)].zfill(8)
    return cRut[:2] + "." + cRut[2:5] + "." + cRut[5:] + "-" + dv


def formatoCorto(cRut):
    # Agrega separador de miles, guión y cero a la izquierda
    cRut = limpia(cRut)
    dv = cRut[-1]
    # Elimina cero a la izquierda
    return str(int(cRut[:-1])) + "-" + dv


def valida(cRut):
    if cRut is None:
        return True
    # Recibe el RUT completo y verifica el DV
    cRut = limpia(cRut)
    if len(cRut) < 8 and len(cRut) > 9:
        return False
    try:
        nRut = int(cRut[0 : len(cRut) - 1])
        if nRut <= 999999:
            return False
    except Exception:
        return False
    dv_a = cRut[-1]
    dv_b = calcDv(str(nRut))
    # print(cRut, nRut, '-', dv_a, '{', dv_b, '}')
    return dv_a == dv_b
