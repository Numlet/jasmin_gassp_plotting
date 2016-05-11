# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 09:53:35 2014

@author: eejvt
"""

import numpy.ma as ma
#import cartopy.crs as ccrs
#import cartopy.feature as cfeat
from scipy.io.idl import readsav
from scipy.optimize import minimize
import scipy as sp
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
from glob import glob
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LogNorm
from matplotlib import colors, ticker, cm

import datetime


def plot(data,title=' ',projection='cyl',file_name=datetime.datetime.now().isoformat(),show=1,cblabel='$\mu g/ m^3$',cmap=plt.cm.RdBu_r,clevs=np.zeros(1),return_fig=0,dpi=300,lon=0,lat=0,colorbar_format_sci=0,saving_format='svg',scatter_points=0,f_size=20):
    # lon_0 is central longitude of projection.

    #clevs=np.logspace(np.amax(data),np.amin(data),levels)
    #print np.amax(data),np.amin(data)
    fig=plt.figure(figsize=(20, 12))
    m = fig.add_subplot(1,1,1)
    # resolution = 'c' means use crude resolution coastlines.
    if projection=='merc':
        m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20)
    else:
        m = Basemap(projection=projection,lon_0=0)
    m.drawcoastlines()

    #m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    #m.drawparallels(np.arange(-90.,120.,10.))
    #m.drawmeridians(np.arange(0.,360.,60.))
    #m.drawmapboundary(fill_color='aqua')
    #if (np.log(np.amax(data))-np.log(np.amin(data)))!=0:
        #clevs=logscale(data)
        #s=m.contourf(X,Y,data,30,latlon=True,cmap=cmap,clevs=clevs)#locator=ticker.LogLocator(),
    #else:
    if isinstance(lon, int):
        lon=readsav('/nfs/a107/eejvt/IDL_CODE/glon.sav')
    if isinstance(lat, int):
        lat=readsav('/nfs/a107/eejvt/IDL_CODE/glat.sav')

        X,Y=np.meshgrid(lon.glon,lat.glat)
    else:
        if lon.ndim==1:
            X,Y=np.meshgrid(lon,lat)
        else:
            X=np.copy(lon)
            Y=np.copy(lat)
    if type(clevs) is list:

        #clevs=clevs.tolist()

        cs=m.contourf(X,Y,data,clevs,latlon=True,cmap=cmap,norm= colors.BoundaryNorm(clevs, 256))
        if colorbar_format_sci:
            cb = m.colorbar(cs,format='%.2e',ticks=clevs)
          
        else:
            cb = m.colorbar(cs,format='%.2e',ticks=clevs)
            #cb.set_ticks(clevs)
            #cb.set_ticklabels(clevs)
        '''
        clevs=logclevs(data)
        print clevs
        if clevs.all()==0:
            cs=m.contourf(X,Y,data,30,latlon=True,cmap=cmap)
        else:
            cs=m.contourf(X,Y,data,30,latlon=True,cmap=cmap,levels=clevs)
            '''
    else:
        cs=m.contourf(X,Y,data,15,latlon=True,cmap=cmap)
        cb = m.colorbar(cs)

    '''
    if clevs.all==0:
        cs=m.contourf(X,Y,data,30,latlon=True,cmap=cmap)
        #m.bluemarble()
        cb = m.colorbar(cs,"right",size="5%", pad="2%")

    else:
        cs=m.contourf(X,Y,data,30,latlon=True,cmap=cmap,clevs=clevs)
        cb = m.colorbar(cs,"right",size="5%", pad="2%")
        '''
    if not isinstance(scatter_points,int):
        m.scatter(scatter_points[:,0],scatter_points[:,100])
    #cb = m.colorbar(cs,"right",ticks=clevs)#,size="5%", pad="2%"
    #cb.set_label(label=cblabel,size=45,weight='bold')#,fontsize=40)
    cb.set_label(cblabel,fontsize=f_size)
    cb.ax.tick_params(labelsize=f_size)#plt.colorbar().set_label(label='a label',size=15,weight='bold')
    plt.title(title,fontsize=f_size)
    if os.path.isdir("PLOTS/"):
        plt.savefig('PLOTS/'+file_name+'.'+saving_format,format=saving_format,dpi=dpi)
        plt.savefig('PLOTS/'+file_name+'.svg',format='svg')
    else:
        plt.savefig(file_name+'.'+saving_format,format=saving_format,dpi=dpi)
        plt.savefig(file_name+'.svg',format='svg')
    if show:
        plt.show()
    #print clevs

    if return_fig:
        return m

