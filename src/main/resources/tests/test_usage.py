import sys
import os
import math
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import cawa_tcwv_land_core
import cawa_tcwv_ocean_core

TSTDIR=os.path.realpath(os.path.dirname(__file__))


def test_it(what='ocean',inst='meris'):
    
    if what == 'ocean':
        if inst == 'meris':
            tcwv_op=cawa_tcwv_ocean_core.ocean_core(TSTDIR+'/../luts/ocean/ocean_core_meris.nc4')
            inp={'suz':10.,
                 'vie':40.,
                 'azi':170.,
                 'amf':1./math.cos(40.*math.pi/180.)+1./math.cos(10.*math.pi/180.),
                 'rtoa':{ '13':0.0045663
                         ,'14':0.00440355
                         ,'15':0.00356704375818},
                 'prior_wsp':10.5,
                 'prior_aot':0.15,
                 'prior_tcwv':10.}
            # Attention: prior windspeed and prior tcwv must come from a 
            # relaible source (e.g. ECMWF ERA). I can provide necessarty data
        elif inst == 'modis_terra':
            tcwv_op=cawa_tcwv_ocean_core.ocean_core(TSTDIR+'/../luts/ocean/ocean_core_modis_terra.nc4')
            inp={'suz':10.,
                 'vie':40.,
                 'azi':170.,
                 'amf':1./math.cos(40.*math.pi/180.)+1./math.cos(10.*math.pi/180.),
                 'rtoa':{'2':0.088780656,
                         '17':0.072717756,
                         '18':0.048099432,
                         '19':0.056601364} ,
                 'prior_wsp':9.,
                 'prior_aot':0.1,
                 'prior_tcwv':15.}
                 
    elif what == 'land':
        if inst == 'meris':
            tcwv_op=cawa_tcwv_land_core.land_core(TSTDIR+'/../luts/land/land_core_meris.nc4')
            inp={'suz':10.,
                 'vie':40.,
                 'azi':170.,
                 'amf':1./math.cos(40.*math.pi/180.)+1./math.cos(10.*math.pi/180.),
                 'prs':1005,
                 'aot':0.1,
                 'tmp':280.,
                 'rtoa':{'13':0.04228669,
                         '14':0.04442161,
                         '15':0.031},
                 'prior_al0':0.13,
                 'prior_al1':0.13,
                 'prior_tcwv':15.}
        if inst == 'modis_terra':
            tcwv_op=cawa_tcwv_land_core.land_core(TSTDIR+'/../luts/land/land_core_modis_terra.nc4')
            inp={'suz':40.,
                 'vie':10.,
                 'azi':170.,
                 'amf':1./math.cos(40.*math.pi/180.)+1./math.cos(10.*math.pi/180.),
                 'prs':1005,
                 'aot':0.1,
                 'tmp':280.,
                 'rtoa':{'2':0.088780656,
                         '17':0.072717756,
                         '18':0.048099432,
                         '19':0.056601364,
                         '5':0.08656} ,
                 'prior_al0':0.13,
                 'prior_al1':0.13,
                 'prior_tcwv':15.}


    
    tt=time.time
    a=tt()
    for i in range(1000): _=tcwv_op.estimator(inp)['res'].x
    print '     %s, %s: %i us'%(what,inst,(tt()-a)*1000.)

     
 
if __name__=='__main__':
    for inst in ('meris','modis_terra'):
        for what in ('ocean','land'):
            test_it(what,inst)