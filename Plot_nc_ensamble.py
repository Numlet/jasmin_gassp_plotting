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

data_path='/group_workspaces/jasmin2/gassp/myoshioka/um/GASSP_PPEs/2008/Variables/'
folder_plots='/group_workspaces/jasmin2/gassp/jvergaratemprado/masaru_nc_plots/'
variables=glob(data_path+'*')
variables=[variable[len(data_path):]+'/' for variable in variables]
print variables

leeds_folder_plots='/nfs/see-fs-01_users/eejvt/svn_test/plots/'

cmap=plt.cm.OrRd
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
                cube=iris.load(file_name)[0]
                print '----------------------------',file_name, 'couldn\'t be opened \n \n'
                continue
            lon=cube.coord('longitude').points[:]
            lat=cube.coord('latitude').points[:]

            cube_data=cube.data[:,0,:,:,:]

            mean_values=cube_data.mean(axis=0)
            std_values=cube_data.std(axis=0)

            file_name_plot=folder_plots+nc_file+'_plot_surface_mean'
            print file_name_plot
            jl.plot(mean_values[0,:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='png',cmap=cmap,show=0)
            plt.close()
            jl.plot(mean_values[0,:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='ps',cmap=cmap,show=0)
            plt.close()
            jl.plot(mean_values[0,:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='pdf',cmap=cmap,show=0)
            plt.close()
            jl.plot(mean_values[0,:,:],title='Mean '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,cmap=cmap)
            plt.close()

            file_name_plot=folder_plots+nc_file+'_plot_surface_std'
            jl.plot(std_values[0,:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='png',cmap=cmap,show=0)
            plt.close()
            jl.plot(std_values[0,:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='ps',cmap=cmap,show=0)
            plt.close()
            jl.plot(std_values[0,:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,saving_format='pdf',cmap=cmap,show=0)
            plt.close()
            jl.plot(std_values[0,:,:],title='Std '+cube.long_name,lat=lat,lon=lon,cblabel=cube.units.origin,file_name=file_name_plot,cmap=cmap)
            plt.close()
leeds_profile='eejvt@see-gw-01.leeds.ac.uk'
command='scp '+folder_plots+'* '+leeds_profile+':'+leeds_folder_plots
os.system(command)
