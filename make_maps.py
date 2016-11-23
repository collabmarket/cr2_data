#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import simplekml
from cr2 import *

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

if __name__ == '__main__':
    make_folders()
    prec = Cr2('p')
    data2kml(prec)
    caud = Cr2('q')
    data2kml(caud)
    temp = Cr2('t')
    data2kml(temp)
    tmin = Cr2('tmin')
    data2kml(tmin)
    tmax = Cr2('tmax')
    data2kml(tmax)
