import json
import pygmaps
import sys
import subprocess
from distance import haversine as getDistance

def findByName (name, features):
    for f in features :
        if name.lower() in f['properties']['nombre'].lower() : return f

def findInRadius (monumento, tuits, radius):
    lon, lat = monumento['geometry']['coordinates']
    return [ tuit for tuit in tuits if getDistance(lon, lat, **tuit['coordenadas']) <= radius]

def buildMap(monumento, tuits, radio):
    lon, lat = monumento['geometry']['coordinates']

    mymap = pygmaps.maps(lat, lon, 16)

    mymap.addpoint(lat, lon, '#00BBFF')
    mymap.addradpoint(lat, lon, radio, '#00BBFF')

    for tuit in tuits : mymap.addpoint(tuit['coordenadas']['latitud'], tuit['coordenadas']['longitud'], '#FFBB00')
    build(mymap, './index.html')

def build(mm, path):
    mm.draw(path)
    print "Mapa disponible en  http://localhost:8000"
    subprocess.Popen('python -m SimpleHTTPServer 8000', shell= True)
    subprocess.Popen('python -m webbrowser -t "http://localhost:8000/"', shell=True)

with open('monumentos-reducido.json', 'r') as mon, open('tuits.json', 'r') as tui:
    monuments, tuits = [json.load(mon), json.load(tui)]

allFeatures = monuments['features']

nameFind = raw_input('Introduce un nombre a buscar : ')
searchedFeature = findByName(nameFind, allFeatures)
if not searchedFeature :
    print 'No se ha encontrado ning?n monumento... Saliendo del programa.'
    sys.exit(1)
#print searchedFeature
radioFind = float(raw_input('Introduce un radio de b?squeda : '))
searchedTuits = findInRadius(searchedFeature, tuits['tuits'], radioFind)
#print len(searchedTuits)
buildMap(searchedFeature, searchedTuits, radioFind)



##### SEGUNDA TAREA
print 'Analysis...'
analysis = {}
analysis['analysis'] = []
maxDistance = float(raw_input('Dame una distancia m?xima : '))
for monum in allFeatures:
    lon, lat = monum['geometry']['coordinates']
    mo = {}
    mo['idnotes'] = monum['properties']['idnotes']
    mo['num_tweets'] = len([ tuit for tuit in tuits['tuits'] if getDistance(lon, lat, **tuit['coordenadas']) <= maxDistance])
    analysis['analysis'].append(mo)

print analysis


## TERCERA TAREA
wordHashtag = raw_input('Introduce un hashtag')
tuitsWithHashtag = [tuit for tuit in tuits['tuits'] if wordHashtag in tuit['hashtags']]
lons = [ tuit['coordenadas']['longitud'] for tuit in tuitsWithHashtag ]
lats = [ tuit['coordenadas']['latitud'] for tuit in tuitsWithHashtag ]
lon = reduce(lambda a, b : a + b, lons) / len(lons)
lat = reduce(lambda a, b : a + b, lats) / len(lats)
mymap2 = pygmaps.maps(lat, lon, 16)
for tuit in tuitsWithHashtag : mymap2.addpoint(tuit['coordenadas']['latitud'], tuit['coordenadas']['longitud'], '#FFBB00')
build(mymap2, './hashtags.html')
subprocess.Popen('python -m webbrowser -t "http://localhost:8000/hashtags.html"', shell=True)

