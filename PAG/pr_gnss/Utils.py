#!/usr/bin/python
# -*- coding: utf8 -*-

from math import pi

class Utils(object):
    @staticmethod
    def UTC2GPS(fecha):
        '''
        @UTC2GPS: Método estático para convertir un objeto de la clase datetime a tiempo GPS
        @fecha datetime: Objeto de la clase datetime con la fecha a transformar en tiempo GPS.
        '''
        ## Obtenemos el número del día
        ## En python el día 0 es el lunes
        day = fecha.weekday()
        ## Si el día es Domingo (número 6) -> día = -1
        if day == 6 : day = -1
        ## Calculamos el tiempo GPS
        return ( (day + 1) * 86400 ) + int(fecha.strftime('%H')) * 3600 + int(fecha.strftime('%M')) * 60 + int(fecha.strftime('%S'))

def main():
    from datetime import datetime
    print(Utils.UTC2GPS(datetime(2014,11,2,17,0,0)))

if __name__=="__main__":
    main()