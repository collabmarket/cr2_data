import os
from cr2 import *

def make_folders():
    root = 'plots'
    folders = ['prec', 'caud', 'temp', 'tmin', 'tmax']
    subfolders = ['annual', 'simple', 'month']
    
    if not os.path.exists(root):
        os.mkdir(root)
    for folder in folders:
        fold = os.path.join(root, folder)
        if not os.path.exists(fold):
            os.mkdir(fold)
        for subfolder in subfolders:
            subfold = os.path.join(fold, subfolder)
            if not os.path.exists(subfold):
                os.mkdir(subfold)

def plots_prec(prec):
    for istation in prec.df.columns:
        filename = 'plots/prec/annual/%s_annual.png'%(istation)
        prec.plot_annual(istation, filename=filename)
        filename = 'plots/prec/simple/%s_simple.png'%(istation)
        prec.plot_simple(istation, filename=filename)
        filename = 'plots/prec/month/%s_month.png'%(istation)
        prec.plot_month(istation, filename=filename)

def plots_caud(caud):
    for istation in caud.df.columns:
        filename = 'plots/caud/annual/%s_annual.png'%(istation)
        caud.plot_annual(istation, filename=filename)
        filename = 'plots/caud/simple/%s_simple.png'%(istation)
        caud.plot_simple(istation, filename=filename)
        filename = 'plots/caud/month/%s_month.png'%(istation)
        caud.plot_month(istation, filename=filename)

def plots_temp(temp):
    for istation in temp.df.columns:
        filename = 'plots/temp/annual/%s_annual.png'%(istation)
        temp.plot_annual(istation, filename=filename)
        filename = 'plots/temp/simple/%s_simple.png'%(istation)
        temp.plot_simple(istation, filename=filename)
        filename = 'plots/temp/month/%s_month.png'%(istation)
        temp.plot_month(istation, filename=filename)

def plots_tmin(tmin):
    for istation in tmin.df.columns:
        filename = 'plots/tmin/annual/%s_annual.png'%(istation)
        tmin.plot_annual(istation, filename=filename)
        filename = 'plots/tmin/simple/%s_simple.png'%(istation)
        tmin.plot_simple(istation, filename=filename)
        filename = 'plots/tmin/month/%s_month.png'%(istation)
        tmin.plot_month(istation, filename=filename)

def plots_tmax(tmax):
    for istation in tmax.df.columns:
        filename = 'plots/tmax/annual/%s_annual.png'%(istation)
        tmax.plot_annual(istation, filename=filename)
        filename = 'plots/tmax/simple/%s_simple.png'%(istation)
        tmax.plot_simple(istation, filename=filename)
        filename = 'plots/tmax/month/%s_month.png'%(istation)
        tmax.plot_month(istation, filename=filename)

if __name__ == '__main__':
    make_folders()
    prec = Cr2('p')
    plots_prec(prec)
    caud = Cr2('q')
    plots_caud(caud)
    temp = Cr2('t')
    plots_temp(temp)
    tmin = Cr2('tmin')
    plots_tmin(tmin)
    tmax = Cr2('tmax')
    plots_tmax(tmax)
