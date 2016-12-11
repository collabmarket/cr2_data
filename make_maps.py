#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from cr2 import *

try:
    import simplekml
except ImportError, e:
    if str(e) == 'No module named simplekml':
        print('simplekml not installed, data2kml will not work!')
    else:
        raise
try:
    import geojson
except ImportError, e:
    if str(e) == 'No module named geojson':
        print('geojson not installed, data2geojson will not work!')
    else:
        raise

root = 'maps'

def make_folders():
    if not os.path.exists(root):
        os.mkdir(root)

def data2kml(variable):
    filename = os.path.join(root, 'stations-%s.kml'%variable.var)
    kml = simplekml.Kml()
    variable.meta.T.apply(lambda X: kml.newpoint(
            name=X["codigo_estacion"], 
            description=unicode(X["nombre"].decode('utf8')), 
            coords=[( X["longitud"], X["latitud"], X["altura"])]) , axis=1)
    kml.save(path=filename)

def data2geojson(variable):
    filename = os.path.join(root, 'stations-%s.geojson'%variable.var)
    features = []
    variable.meta.T.apply(lambda X: features.append( 
            geojson.Feature(geometry=geojson.Point((
                                            float(X["longitud"]), 
                                            float(X["latitud"]), 
                                            float(X["altura"]))), 
                properties=dict(name=X["codigo_estacion"], 
                                description=unicode(X["nombre"].decode('utf8')))
                            )
                                                    )
                  , axis=1)
    with open(filename, 'w') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True)

if __name__ == '__main__':
    make_folders()
    prec = Cr2('monthly', 'p', 'data.json')
    caud = Cr2('monthly', 'q', 'data.json')
    temp = Cr2('monthly', 't', 'data.json')
    tmin = Cr2('monthly', 'tmin', 'data.json')
    tmax = Cr2('monthly', 'tmax', 'data.json')
    data2kml(prec)
    data2kml(caud)
    data2kml(temp)
    data2kml(tmin)
    data2kml(tmax)
    data2geojson(prec)
    data2geojson(caud)
    data2geojson(temp)
    data2geojson(tmin)
    data2geojson(tmax)
