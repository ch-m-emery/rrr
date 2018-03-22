#!/usr/bin/env python2
#*******************************************************************************
#rrr_cpl_riv_lsm_err.py
#*******************************************************************************

#Purpose:
#Given one file with estimates of time-varying external inflow (in m^3) into the
#river network, and another similar file assumed to contain the "true" values of
#the same quantities, this program computes the corresponding bias, standard 
#error, and error convariances and saves these values in a new netCDF file.
#Author:
#Cedric H. David, 2018-2018


#*******************************************************************************
#Import Python modules
#*******************************************************************************
import sys
import netCDF4
import numpy


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - rrr_vol_mod
# 2 - rrr_vol_tru
# 3 - rrr_vol_err


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg != 4:
     print('ERROR - 3 and only 3 arguments must be used')
     raise SystemExit(22) 

rrr_vol_mod=sys.argv[1]
rrr_vol_tru=sys.argv[2]
rrr_vol_err=sys.argv[3]


#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print('- '+rrr_vol_mod)
print('- '+rrr_vol_tru)
print('- '+rrr_vol_err)


#*******************************************************************************
#Check if files exist 
#*******************************************************************************
try:
     with open(rrr_vol_mod) as file:
          pass
except IOError as e:
     print('ERROR - Unable to open '+rrr_vol_mod)
     raise SystemExit(22) 

try:
     with open(rrr_vol_tru) as file:
          pass
except IOError as e:
     print('ERROR - Unable to open '+rrr_vol_tru)
     raise SystemExit(22) 


#*******************************************************************************
#Reading netCDF file 1
#*******************************************************************************
print('Reading netCDF file 1')

#-------------------------------------------------------------------------------
#Open netCDF file
#-------------------------------------------------------------------------------
f1 = netCDF4.Dataset(rrr_vol_mod, 'r')

#-------------------------------------------------------------------------------
#Get dimension sizes
#-------------------------------------------------------------------------------
if 'COMID' in f1.dimensions:
     YS_rivid1='COMID'
elif 'rivid' in f1.dimensions:
     YS_rivid1='rivid'
else:
     print('ERROR - Neither COMID nor rivid exist in '+rrr_vol_mod)
     raise SystemExit(22) 

IS_riv_tot1=len(f1.dimensions[YS_rivid1])
print('- The number of river reaches is: '+str(IS_riv_tot1))

if 'Time' in f1.dimensions:
     YS_time1='Time'
elif 'time' in f1.dimensions:
     YS_time1='time'
else:
     print('ERROR - Neither Time nor time exist in '+rrr_vol_mod)
     raise SystemExit(22) 

IS_time1=len(f1.dimensions[YS_time1])
print('- The number of time steps is: '+str(IS_time1))

#-------------------------------------------------------------------------------
#Get variables
#-------------------------------------------------------------------------------
if 'm3_riv' in f1.variables:
     YS_var1='m3_riv'
else:
     print('ERROR - m3_riv does not exist in '+rrr_vol_mod)
     raise SystemExit(22) 

IV_riv_tot_id1=f1.variables[YS_rivid1][:]
ZV_time1=f1.variables[YS_time1][:]

if '_FillValue' in  f1.variables[YS_var1].ncattrs(): 
     ZS_fill1=f1.variables[YS_var1]._FillValue
     print('- The fill value is: '+str(ZS_fill1))
else:
     ZS_fill1=None

if 'long_name' in  f1.variables[YS_var1].ncattrs(): 
     YS_long_name1=f1.variables[YS_var1].long_name
else:
     YS_long_name1=None

if 'units' in  f1.variables[YS_var1].ncattrs(): 
     YS_units1=f1.variables[YS_var1].units
else:
     YS_units1=None

if 'coordinates' in  f1.variables[YS_var1].ncattrs(): 
     YS_coordinates1=f1.variables[YS_var1].coordinates
else:
     YS_coordinates1=None

if 'grid_mapping' in  f1.variables[YS_var1].ncattrs(): 
     YS_grid_mapping1=f1.variables[YS_var1].grid_mapping
else:
     YS_grid_mapping1=None

if 'cell_methods' in  f1.variables[YS_var1].ncattrs(): 
     YS_cell_methods1=f1.variables[YS_var1].cell_methods
else:
     YS_cell_methods1=None


#*******************************************************************************
#Reading netCDF file 2
#*******************************************************************************
print('Reading netCDF file 2')

#-------------------------------------------------------------------------------
#Open netCDF file
#-------------------------------------------------------------------------------
f2 = netCDF4.Dataset(rrr_vol_tru, 'r')

#-------------------------------------------------------------------------------
#Get dimension sizes
#-------------------------------------------------------------------------------
if 'COMID' in f2.dimensions:
     YS_rivid2='COMID'
elif 'rivid' in f2.dimensions:
     YS_rivid2='rivid'
else:
     print('ERROR - Neither COMID nor rivid exist in '+rrr_vol_tru)
     raise SystemExit(22) 

IS_riv_tot2=len(f2.dimensions[YS_rivid2])
print('- The number of river reaches is: '+str(IS_riv_tot2))

if 'Time' in f2.dimensions:
     YS_time2='Time'
elif 'time' in f2.dimensions:
     YS_time2='time'
else:
     print('ERROR - Neither Time nor time exist in '+rrr_vol_tru)
     raise SystemExit(22) 

IS_time2=len(f2.dimensions[YS_time2])
print('- The number of time steps is: '+str(IS_time2))

#-------------------------------------------------------------------------------
#Get variables
#-------------------------------------------------------------------------------
if 'm3_riv' in f2.variables:
     YS_var2='m3_riv'
else:
     print('ERROR - m3_riv does not exist in '+rrr_vol_tru)
     raise SystemExit(22) 

IV_riv_tot_id2=f2.variables[YS_rivid2][:]
ZV_time2=f2.variables[YS_time2][:]

if '_FillValue' in  f2.variables[YS_var2].ncattrs(): 
     ZS_fill2=f2.variables[YS_var2]._FillValue
     print('- The fill value is: '+str(ZS_fill2))
else:
     ZS_fill2=None

if 'long_name' in  f2.variables[YS_var2].ncattrs(): 
     YS_long_name2=f2.variables[YS_var2].long_name
else:
     YS_long_name2=None

if 'units' in  f2.variables[YS_var2].ncattrs(): 
     YS_units2=f2.variables[YS_var2].units
else:
     YS_units2=None

if 'coordinates' in  f2.variables[YS_var2].ncattrs(): 
     YS_coordinates2=f2.variables[YS_var2].coordinates
else:
     YS_coordinates2=None

if 'grid_mapping' in  f2.variables[YS_var2].ncattrs(): 
     YS_grid_mapping2=f2.variables[YS_var2].grid_mapping
else:
     YS_grid_mapping2=None

if 'cell_methods' in  f2.variables[YS_var2].ncattrs(): 
     YS_cell_methods2=f2.variables[YS_var2].cell_methods
else:
     YS_cell_methods2=None


#*******************************************************************************
#Check consistency
#*******************************************************************************
print('Check consistency')

if IS_riv_tot1==IS_riv_tot2: 
     IS_riv_tot=IS_riv_tot1
     print('- Common number of river reaches: '+str(IS_riv_tot))
else: 
     print('ERROR - The number of river reaches differ')
     raise SystemExit(22) 
     
if IS_time1==IS_time2: 
     IS_time=IS_time1
     print('- Common number of time steps: '+str(IS_time))
else: 
     print('ERROR - The number of time steps differ')
     raise SystemExit(22) 
     
if (IV_riv_tot_id1==IV_riv_tot_id2).all(): 
     IV_riv_tot_id=IV_riv_tot_id1
     print('- The river reach IDs are the same')
else: 
     print('ERROR - The river reach IDs differ')
     raise SystemExit(22) 
     
if (ZV_time1==ZV_time2).all():
     ZV_time=ZV_time1
     print('- The time variables are the same')
else: 
     print('ERROR - The time variables differ')
     raise SystemExit(22) 
     

#*******************************************************************************
#Computing estimates of error
#*******************************************************************************
print('Computing estimates of error')

#-------------------------------------------------------------------------------
#Computing biases
#-------------------------------------------------------------------------------
print('- Computing biases')

ZV_vol_av1=numpy.empty(IS_riv_tot)
ZV_vol_av2=numpy.empty(IS_riv_tot)
ZV_vol_bia=numpy.empty(IS_riv_tot)

for JS_time in range(IS_time):
     ZV_vol_in1=f1.variables[YS_var1][JS_time,:]
     ZV_vol_in2=f2.variables[YS_var2][JS_time,:]

     ZV_vol_av1=ZV_vol_av1+ZV_vol_in1
     ZV_vol_av2=ZV_vol_av2+ZV_vol_in2

ZV_vol_av1=ZV_vol_av1/IS_time
ZV_vol_av2=ZV_vol_av2/IS_time
ZV_vol_bia=ZV_vol_av1-ZV_vol_av2

#-------------------------------------------------------------------------------
#Computing standard errors
#-------------------------------------------------------------------------------
print('- Computing standard errors')

ZV_vol_dif=numpy.empty(IS_riv_tot)
ZV_vol_sde=numpy.empty(IS_riv_tot)

for JS_time in range(IS_time):
     ZV_vol_in1=f1.variables[YS_var1][JS_time,:]
     ZV_vol_in2=f2.variables[YS_var2][JS_time,:]

     ZV_vol_dif=(ZV_vol_in1-ZV_vol_av1)-(ZV_vol_in2-ZV_vol_av2)
     ZV_vol_sde=ZV_vol_sde+numpy.square(ZV_vol_dif)

ZV_vol_sde=ZV_vol_sde/(IS_time-1)
ZV_vol_sde=numpy.sqrt(ZV_vol_sde)

#-------------------------------------------------------------------------------
#Computing error covariances
#-------------------------------------------------------------------------------
print('- Computing error covariances')

ZM_vol_in1=f1.variables[YS_var1][:,:]
ZM_vol_in2=f2.variables[YS_var2][:,:]
ZM_vol_dif=ZM_vol_in1-ZM_vol_in2

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Check the previous standard error computation from the variance equations
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ZV_vol_sd2=numpy.empty(IS_riv_tot)

for JS_riv_tot in range(IS_riv_tot):
     ZV_vol_dif=ZM_vol_dif[:,JS_riv_tot]
     ZV_vol_sd2[JS_riv_tot]=numpy.dot(ZV_vol_dif-ZV_vol_dif.mean(),            \

                                      ZV_vol_dif-ZV_vol_dif.mean())
ZV_vol_sd2=ZV_vol_sd2/(IS_time-1)
ZV_vol_sd2=numpy.sqrt(ZV_vol_sd2)

ZS_rdif_max=0
for JS_riv_tot in range(IS_riv_tot):
     if ZV_vol_sde[JS_riv_tot]!=0:
          ZS_rdif=abs((ZV_vol_sd2[JS_riv_tot]-ZV_vol_sde[JS_riv_tot])          \
                      /ZV_vol_sde[JS_riv_tot])
          ZS_rdif_max=max(ZS_rdif_max,ZS_rdif)

if ZS_rdif_max<=5e-6:
     print(' . Acceptable max relative difference in standard errors using two'\
          +' different methods: '+str(ZS_rdif_max))
else:
     print('ERROR - Unacceptable max relative difference in standard errors '  \
           'using two different methods')
     raise SystemExit(22)

#-------------------------------------------------------------------------------
#Close netCDF files
#-------------------------------------------------------------------------------
f1.close()
f2.close()


#*******************************************************************************
#Printing some diagnostic quantities
#*******************************************************************************
print('Printing some diagnostic quantities')

#-------------------------------------------------------------------------------
#Basic quantities
#-------------------------------------------------------------------------------
YS_str=str(numpy.round(ZV_vol_av1.mean(),2))
print('- Spatial and temporal mean of model:          '+YS_str)
YS_str=str(numpy.round(ZV_vol_av2.mean(),2))
print('- Spatial and temporal mean of ensemble:       '+YS_str)
YS_str=str(numpy.round(ZV_vol_bia.mean(),2))
print('- Spatial and temporal mean of bias:           '+YS_str)
YS_str=str(numpy.round(ZV_vol_sde.mean(),2))
print('- Spatial and temporal mean of standard error: '+YS_str)

#-------------------------------------------------------------------------------
#More advanced quantities
#-------------------------------------------------------------------------------
ZV_vol_av1[ZV_vol_av1==0]=numpy.nan

ZS_str=numpy.nanmedian(numpy.abs((numpy.divide(ZV_vol_bia,ZV_vol_av1))))
YS_str=str(numpy.round(ZS_str,2))
print('- Median ratio of bias over model              '+YS_str) 
ZS_str=numpy.nanmedian(numpy.abs((numpy.divide(ZV_vol_sde,ZV_vol_av1))))
YS_str=str(numpy.round(ZS_str,2))
print('- Median ratio of standard error over model    '+YS_str) 


#*******************************************************************************
#End
#*******************************************************************************