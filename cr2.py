#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import pandas as pd
import matplotlib.pyplot as plt

class Cr2:
    '''
    p='Precipitacion', q='Caudal',
    t='Temperatura', tmax='Temperatura max', tmin='Temperatura min'
    '''
    def __init__(self, period, var, sourcefile):
        sources = self.open_sources(sourcefile, period, var)
        self.var = sources['var']
        self.varname = sources['varname']
        self.filename = sources['filename']
        self.units = sources['units']
        self.df = self.get_df(sources['filename'])
        self.meta = self.get_meta(sources['filename'])

    def open_sources(self, sourcefile, period, var):
        with open(sourcefile) as data_file:
            sources = json.load(data_file)
        root = sources.keys().pop()
        items = sources[root][period]
        for item in items:
            if item['var'] == var:
                item['filename'] = os.path.join(root, 
                                                period, 
                                                item['filename'], 
                                                item['filename']+'.txt')
                return item
    
    def iname(self, column='nombre'):
        return dict(zip(self.df.columns.tolist(), self.meta.T.loc[:,column].tolist()))
    
    def kname(self, column='nombre'):
        return dict(zip(self.meta.T.loc[:,column].tolist(), self.df.columns.tolist()))
    
    def get_df(self, filename):
        # Create meta and df
        df = pd.read_csv(filename, skiprows=14, header=None)
        
        # Curate df
        df.set_index(0, inplace=True)
        df.index = pd.to_datetime(df.index)
        df.replace(-9999.0, pd.np.nan, inplace=True)
        df.columns.name = df.index.name
        df.index.name = 'Date'
        return df
    
    def get_meta(self, filename):
        # Create meta and df
        meta = pd.read_csv(filename, nrows=14, header=None)
        # Curate meta
        meta = meta.T
        meta.columns = meta.iloc[0]
        meta = meta.reindex(meta.index.drop(0))
        meta.inicio_observaciones = pd.to_datetime(meta.inicio_observaciones)
        meta.fin_observaciones = pd.to_datetime(meta.fin_observaciones)
        meta.altura = pd.to_numeric(meta.altura)
        meta.cantidad_observaciones = pd.to_numeric(meta.cantidad_observaciones)
        meta = meta.T
        return meta
    
    def busca(self, pattern, column='nombre'):
        return self.meta.T[self.meta.T.loc[:,column].str.contains(pattern)]
    
    def plot_simple(self, istation, filename=None, figsize=(10, 7.5)):
        # Plot simple
        fig, ax = plt.subplots(facecolor='w', figsize=figsize)
        station = unicode(self.iname()[istation].decode('utf8'))
        titulo = '%s  %s'%(self.varname, station)
        plotkarg = dict(title=titulo, ax=ax, style='x')
        self.df.loc[:,istation].dropna().plot(**plotkarg)
        ax.set_ylabel('%s %s'%(self.var, self.units))
        if filename:
            fig.savefig('%s'%(filename), bbox_inches='tight')
        else:
            plt.show()
        plt.close(fig) # Fix Warning: More than 20 figures have been opened
    
    def plot_month(self, istation, filename=None, figsize=(10, 7.5)):
        fig, ax = plt.subplots(facecolor='w', figsize=figsize)
        station = unicode(self.iname()[istation].decode('utf8'))
        titulo = '%s mensual promedio %s'%(self.varname, station)
        # Lista meses del agno
        months = [pd.datetime(2000, i, 1).strftime('%B') for i in range(1,13)]
        aux = self.df.loc[:,istation].dropna()
        aux = aux.groupby(aux.index.month).mean()
        aux.index = months
        if self.var in ['p','q']:
            # Plot promedio cada mes
            plotkarg = dict(kind='bar', title=titulo, rot=45, ax=ax)
            aux.plot(**plotkarg)
        else:
            # Plot promedio cada mes
            plotkarg = dict(title=titulo, rot=45, ax=ax)
            aux.plot(**plotkarg)
        ax.set_ylabel('%s %s'%(self.var, self.units))
        if filename:
            fig.savefig('%s'%(filename), bbox_inches='tight')
        else:
            plt.show()
        plt.close(fig) # Fix Warning: More than 20 figures have been opened
    
    def plot_annual(self, istation, filename=None, figsize=(10, 7.5)):
        # Plot prec anual
        fig, ax = plt.subplots(facecolor='w', figsize=figsize)
        station = unicode(self.iname()[istation].decode('utf8'))
        titulo = '%s anual %s'%(self.varname, station)
        plotkarg = dict(kind='bar', title=titulo, ax=ax)
        if self.var == 'p':
            aux = self.df.loc[:,istation].dropna().resample('A').sum()
        else:
            aux = self.df.loc[:,istation].dropna().resample('A').mean()
        aux.plot(**plotkarg)
        ax.axhline(y=aux.mean(), color='r', linestyle='--')
        ax.set_ylabel('%s %s'%(self.var, self.units))
        xtl = [item.get_text()[:4] for item in ax.get_xticklabels()]
        _ = ax.set_xticklabels(xtl)
        if filename:
            fig.savefig('%s'%(filename), bbox_inches='tight')
        else:
            plt.show()
        plt.close(fig) # Fix Warning: More than 20 figures have been opened
        

def plot_climograph(prec, temp, cod_station, filename=None, figsize=(10, 7.5)):
    try:
        iprec = prec.kname('codigo_estacion')[cod_station]
    except KeyError:
        print("Codigo estacion no se encuentra en %s"%prec.varname)
        raise
    try:
        itemp = temp.kname('codigo_estacion')[cod_station]
    except KeyError:
        print("Codigo estacion no se encuentra en %s"%temp.varname)
        raise
    if prec.var == 'p' and temp.var == 't':
        graphtype = 'Climograma'
    else:
        graphtype = 'Grafo'
    station = unicode(prec.iname()[iprec].decode('utf8'))
    titulo = '%s %s %s'%(cod_station, graphtype, station)
    months = [pd.datetime(2000, i, 1).strftime('%B') for i in range(1,13)]
    df = pd.DataFrame()
    aux = prec.df.loc[:,iprec].dropna()
    df[prec.var] = aux.groupby(aux.index.month).mean()
    aux = temp.df.loc[:,itemp].dropna()
    df[temp.var] = aux.groupby(aux.index.month).mean()
    df.index = months
    fig, ax = plt.subplots(facecolor='w', figsize=figsize)
    ax2 = ax.twinx()
    plotkarg = dict(kind='bar', rot=90, title=titulo, ax=ax)
    df.loc[:,prec.var].plot(**plotkarg)
    plotkarg = dict(color='r', ax=ax2)
    df.loc[:,temp.var].plot(**plotkarg)
    # Switch the place of the secondary and axis
    ax.yaxis.tick_right()
    ax2.yaxis.tick_left()
    # Put label on the contrary after switch
    ax2.set_ylabel('%s %s'%(prec.var, prec.units))
    ax2.yaxis.labelpad = 25 # Fixed label position after switch
    ax.set_ylabel('%s %s'%(temp.var, temp.units))
    ax.yaxis.labelpad = 25 # Fixed label position after switch
    if filename:
        fig.savefig('%s'%(filename), bbox_inches='tight')
    else:
        plt.show()
    plt.close(fig) # Fix Warning: More than 20 figures have been opened


if __name__ == '__main__':
    try:
        get_ipython().magic(u'matplotlib inline')
    except NameError:
        print "IPython console not available."
    prec = Cr2('monthly', 'p', 'data.json')
    caud = Cr2('monthly', 'q', 'data.json')
    temp = Cr2('monthly', 't', 'data.json')
    tmin = Cr2('monthly', 'tmin', 'data.json')
    tmax = Cr2('monthly', 'tmax', 'data.json')
