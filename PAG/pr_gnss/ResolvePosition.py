#!/usr/bin/python
# -*- coding: utf8 -*-

from ObsParser import ObservationParser
from NavParser import NavigationParser
from Utils import Utils

class Solver(object) :

    def __init__(self, navParser, obsParser) :
        if not isinstance(navParser, NavigationParser) : raise Exception('navParser debe ser del tipo NavigationParser')
        if not isinstance(obsParser, ObservationParser) : raise Exception('navParser debe ser del tipo NavigationParser')

        self.navigation = navParser
        self.observation = obsParser

        self.__calc()

    def __calc(self):
        for obs in self.observation.getObservations():
            ## Obtener la efeméride más cercana para el observable
            for sat in obs['OBSERVACIONES'].keys():
                observation = obs['OBSERVACIONES'][sat]
                #print observation
                #print obs['EPOCA']
                #print observation
                #print sat

                ## Tobservación
                tobs = obs['EPOCA']
                efem = self.navigation.getParams(tobs, sat)
                if not efem : continue
                
                ##trec = tobs - 


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