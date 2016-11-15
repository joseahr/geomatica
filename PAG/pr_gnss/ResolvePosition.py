#!/usr/bin/python
# -*- coding: utf8 -*-

from ObsParser import ObservationParser
from NavParser import NavigationParser
from Utils import Utils
from math import sqrt, sin, atan2, cos

class Solver(object) :

    def __init__(self, navParser, obsParser) :
        if not isinstance(navParser, NavigationParser) : raise Exception('navParser debe ser del tipo NavigationParser')
        if not isinstance(obsParser, ObservationParser) : raise Exception('obsParser debe ser del tipo ObservationParser')

        self.navigation = navParser
        self.observation = obsParser

        ## Velocidad de la luz
        self.C = 2.99792458e8
        ## Constante Gravitatoria * Masa de la tierra
        self.GM = 3.986005e14

        self.__calcSatelitesPosition()

    def __calcSatelitesPosition(self):
        for obs in self.observation.getObservations():
            ## De la observación de una época
            ## Para cada satélite
            for sat in obs['OBSERVACIONES'].keys():
                ## Si el satélite es GPS
                if 'G' in sat :
                    ## Cogemos los observables del satélite
                    observation = obs['OBSERVACIONES'][sat]
                    ## Tobservación
                    tobs = obs['EPOCA']
                    ## Efeméride más próxima a nuestra época
                    efem = self.navigation.getParams(tobs, sat)
                    ## Si no hay observable P2 no seguimos
                    if not efem or not 'P2' in observation: continue

                    ## TOE
                    toe = efem['toe']
                    ## Parámetros para el cálculo de la falta de sincronización de los relojes
                    a0, a1, a2 = [ efem['sv_clock_bias'], efem['sv_clock_drift'], efem['sv_clock_drift_rate'] ]
                    ## Semieje mayor de la órbita
                    a = efem['sqrt_a']**2
                    ## Diferencia del movimiento medio respecto al valor calculado
                    delta_n = efem['delta_n']
                    ## Mo = Anomalía media en el tiempo de referencia
                    Mo = efem['mo']
                    ## Excentricidad de la órbita del satélite
                    e = efem['eccentricity']
                    ## Argumento del perigeo
                    w = efem['omega']
                    ## Parámetros para correcciones orbitales Cus, Crs, Cis
                    cus, crs, cis = [ efem['cus'], efem['crs'], efem['cis'] ]
                    cuc, crc, cic = [ efem['cuc'], efem['crc'], efem['cic'] ]
                    ## Inclinación de la órbita en el momento de referencia
                    io = efem['io']
                    ## Variación del ángulo de inclinación de la órbita
                    idot = efem['idot']
                    ## Longitud del nodo ascendente de la órbita
                    ## en la época de la semana de referencia
                    omega_0 = efem['OMEGA']
                    ## Variación de la ascensión recta
                    omega_var = efem['omega_dot']
                    ## Valor de la rotación terrestre
                    omega_e = 7.2921151467e-5

                    ## Cálculo del tiempo de emisión
                    temis = Utils.UTC2GPS(tobs) - (observation['P2']['VALUE']/self.C) - toe

                    tcorr = a0 + a1*temis + a2*temis**2

                    temis = Utils.UTC2GPS(tobs) - (observation['P2']['VALUE']/self.C) - tcorr - toe

                    tcorr = a0 + a1*temis + a2*temis**2
                    temis = Utils.UTC2GPS(tobs) - (observation['P2']['VALUE']/self.C) - tcorr - toe


                    ## Movimiento medio
                    n = sqrt( self.GM / (a**3) ) + delta_n
                    ## M = Anomalía media
                    M = Mo + (n * temis)
                    ## E = Anomalía excéntrica
                    E = Eant = M
                    Eant = 0 ## Variable auxiliar para el proceso iterativo
                    while(abs(E - Eant) > 0.0000000001):
                        Eant = E
                        E = M + ( e * sin(Eant) )

                    ## Anomalía verdadera
                    v = atan2( (sqrt(1 - (e**2) )*sin(E)), (cos(E) - e) )
                    ## Argumento de la latitud
                    arg_lat = v + w
                    
                    ## Términos correctivos de los parámetros orbitales
                    du = cus * sin(2 * arg_lat) + cuc * cos(2 * arg_lat)
                    dr = crs * sin(2 * arg_lat) + crc * cos(2 * arg_lat)
                    di = cis * sin(2 * arg_lat) + cic * cos(2 * arg_lat)

                    ## Argumento de la latitud corregido
                    arg_lat += du
                    ## Radio de la órbita corregido
                    r = a * (1 - e * cos(E)) + dr
                    ## Inclinación de la órbita corregida
                    i = io + di + idot * temis

                    ## Posición del satélite en el plano orbital
                    Xop = r * cos(arg_lat)
                    Yop = r * sin(arg_lat)

                    ## Longitud corregida del nodo ascendente
                    omega = omega_0 + ( (omega_var - omega_e) * temis ) - ( omega_e * toe )

                    ## Coordenadas finales del satélite
                    Xsat = Xop * cos(omega) - Yop * cos(i)*sin(omega)
                    Ysat = Xop * sin(omega) + Yop * cos(i)*cos(omega)
                    Zsat = Yop * sin(i)

                    ## Efecto relativista debido a la elipticidad de la órbita del satélite
                    trel = -2 * sqrt( self.GM * a / self.C ) * e * sin(E)

                    ## TGD (Total Group Delay) o constante instrumental del satélite
                    ttgd_l1 = efem['tgd']
                    ttgd_l2 = 1.65 * ttgd_l1

                    ## Finalmente el tiempo corregido será :
                    tcorr += trel - ttgd_l2
                    printSats = ['G02', 'G04', 'G23']
                    if sat in printSats and Utils.UTC2GPS(obs['EPOCA']) == 135110 :
                        print 'sat', sat
                        print 'obs epoca gps_secs', Utils.UTC2GPS(obs['EPOCA'])
                        print 'epoca nav', efem['epoca']
                        print 'epoca obs', obs['EPOCA']
                        print 'tnav - tobs', efem['epoca'] - tobs
                        print 'toe', toe
                        print 'Temis', temis
                        print 'TcorrF', tcorr
                        print 'Mov. medio', n
                        print 'Anomalía media', M
                        print 'du', du
                        print 'dr', dr
                        print 'di', di
                        print 'u', arg_lat
                        print 'r', r
                        print 'i', i
                        print 'Xop, Yop', Xop, Yop
                        print 'omega', omega
                        print 'Anomalía Excentr.', E
                        print 'Anomalía verdadera', v
                        print 'PosSat', Xsat, Ysat, Zsat
                        print '\n'

## Función principal para probar la clase
def main():
    ## Creamos un objeto de la clase
    navParser = NavigationParser('brdc0590-1.11n')
    obsParser = ObservationParser('89090590-1.11o')

    solver = Solver(navParser, obsParser)


## Si estamos ejecutando directamente
## este fichero la variable __name__ contendrá el valor "__main__"
if __name__=="__main__":
    ## Ejecutamos la función main
	main()