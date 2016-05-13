# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:15:23 2016

@author: eejvt
"""

import sys
#sys.path.append('/nfs/a107/eejvt/PYTHON_CODE')
import numpy as np
import Jesuslib as jl
import os
from scipy.io.idl import readsav
from glob import glob
from scipy.io import netcdf
import matplotlib.pyplot as plt
import scipy as sc
from scipy.stats.stats import pearsonr
from glob import glob
from scipy.io.idl import readsav
from scipy import stats
from scipy.optimize import curve_fit
import scipy
import iris
import matplotlib as mpl
mpl.use('Agg')
iris.FUTURE.netcdf_promote=True

def set_all_index(array):
    indexes=[np.s_[:] for _ in range(array.ndim)]
    return indexes


data_path='/group_workspaces/jasmin2/gassp/myoshioka/um/GASSP_PPEs/2008/Variables/'
folder_plots='/group_workspaces/jasmin2/gassp/jvergaratemprado/masaru_nc_plots/'
variables=glob(data_path+'*')
variables=[variable[len(data_path):]+'/' for variable in variables]
print variables

leeds_folder_plots='/nfs/see-fs-01_users/eejvt/svn_test/plots/'
file_path='/nfs/a201/eejvt/LW_UP_AS_TOA_tebaa-tebgz_pm2008jun.nc'
file_path='/nfs/a201/eejvt/CCN0p2_tebaa-tebiz_pm2008jan_t.nc'
file_path='/nfs/a201/eejvt/N50_tebaa-tebiz_pm2008jan_t.nc'
file_path='/nfs/a201/eejvt/RF_SW_CS_TOA_tebaa-tebiz_pm2008jul.nc'
file_path='/nfs/a201/eejvt/AODs_TOTALebaa-tebiz_pm2008oct.nc'
cmap=plt.cm.OrRd
cube=iris.load(file_path)[0]
#%%
print cube
for variable in variables:
    print variable
    data_variable_path=data_path+variable
    print data_variable_path
    folders=['Hires_N96/','Lores_N48/']
    for folder in folders:
        a=glob(data_variable_path+folder+'*')
        str_a=data_variable_path+folder+'*'
        print str_a
        for nc_file in a :
            print nc_file
            nc_file=nc_file[len(data_variable_path+folder):]
            print nc_file
            file_name=data_variable_path+folder+nc_file
        # mb=netcdf.netcdf_file(file_name,'r')
            try:
                cube=iris.load(file_name)[0]
            except:
                #cube=iris.load(file_name)[0]
                print '----------------------------',file_name, 'couldn\'t be opened \n \n'
                print file_name
                continue
            
            plot_name='2D'
            if any(np.array(cube.data.shape) == 85):
                indx=set_all_index(cube)
                lev_pos=cube.data.shape.index(85)
                #surface level
                indx[lev_pos]=0
                indx=tuple(indx)
                cube=cube[indx]
                plot_name='surface'
            if any(np.array(cube.data.shape) == 6):
                indx=set_all_index(cube)
                
                lev_pos=cube.data.shape.index(3)
                #surface level
                indx[lev_pos]=2
                indx=tuple(indx)
                cube=cube[indx]
                plot_name='550nm'
            while any(np.array(cube.data.shape) == 1):
                indx=set_all_index(cube)
                lev_pos=cube.data.shape.index(1)
                #surface level
                indx[lev_pos]=0
                indx=tuple(indx)
                cube=cube[indx]
                
            
            lon=cube.coord('longitude').points[:]
            lat=cube.coord('latitude').points[:]
            coor_collapse=[coor.var_name for coor in cube.coords() if coor.var_name!='latitude' and coor.var_name!='longitude']
            for coor in coor_collapse:
                try:
                    cube=cube.collapsed(coor,iris.analysis.MEAN)
                    print file_name
                    print 'collapsed on:',coor
                except:
                    #print cube
                    print '--------not collapsed-----'
                    print coor
            #iris.Constraint(model_level_number=10)
            
            cube_data=cube.data
            if cube_data.ndim==3 and cube.shape[1]==145 and cube.shape[2]==192:
                print 'nruns=', cube_data.shape[0]
            else:
                print 'cube not with the right dimensions', cube.shape
                continue
                            
            mean_values=cube_data.mean(axis=0)
            std_values=cube_data.std(axis=0)
            file_name_plot=folder_plots+nc_file+'_plot_'+plot_name+'_mean'
            print file_name_plot
            jl.plot(mean_values[:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='png',cmap=cmap,show=0)
            plt.close()
            jl.plot(mean_values[:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='ps',cmap=cmap,show=0)
            plt.close()
            jl.plot(mean_values[:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='pdf',cmap=cmap,show=0)
            plt.close()
            jl.plot(mean_values[:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,cmap=cmap)
            plt.close()

            file_name_plot=folder_plots+nc_file+'_plot_'+plot_name+'_std'
            jl.plot(std_values[:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='png',cmap=cmap,show=0)
            plt.close()
            jl.plot(std_values[:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='ps',cmap=cmap,show=0)
            plt.close()
            jl.plot(std_values[:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='pdf',cmap=cmap,show=0)
            plt.close()
            jl.plot(std_values[:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,cmap=cmap)
            plt.close()
leeds_profile='eejvt@see-gw-01.leeds.ac.uk'
command='scp '+folder_plots+'* '+leeds_profile+':'+leeds_folder_plots
os.system(command)
