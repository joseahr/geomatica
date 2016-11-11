from math import radians, sin, cos, asin, sqrt

def haversine(lon1, lat1, longitud, latitud):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Ouput in meters
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, longitud, latitud])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    #print lon1, lat1, longitud, latitud, km*1000
    return km*1000
