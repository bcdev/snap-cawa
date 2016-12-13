import sys
import os
import math
import time


def test_it(what='ocean',inst='meris'):

    parent_dir = os.path.dirname(os.path.normpath(os.path.dirname(__file__)))
    sys.path.append(parent_dir + '/libs')

    import cawa_tcwv_core as cawa_core
    import cawa_tcwv_land as cawa_land
    import cawa_tcwv_ocean as cawa_ocean

    if what == 'ocean':
        if inst == 'meris':
            ocean_lut=os.path.join(parent_dir, 'luts', 'ocean', 'ocean_core_meris.nc4')
            tcwv_op = cawa_ocean.CawaTcwvOceanCore(ocean_lut)

            inp={'suz':10.,
                 'vie':40.,
                 'azi':170.,
                 'amf':1./math.cos(40.*math.pi/180.)+1./math.cos(10.*math.pi/180.),
                 'rtoa':{ '13':0.0045663,
                         '14':0.00440355,
                         '15':0.00356704375818},
                 'prior_wsp':10.5,
                 'prior_aot':0.15,
                 'prior_tcwv':10.}
            # Attention: prior windspeed and prior tcwv must come from a 
            # relaible source (e.g. ECMWF ERA). I can provide necessarty data
        elif inst == 'modis_terra':
            ocean_lut=os.path.join(parent_dir, 'luts', 'ocean', 'ocean_core_modis_terra.nc4')
            tcwv_op = cawa_ocean.CawaTcwvOceanCore(ocean_lut)

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
            land_lut=os.path.join(parent_dir, 'luts', 'land', 'land_core_meris.nc4')
            tcwv_op = cawa_land.CawaTcwvLandCore(land_lut)

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
            land_lut=os.path.join(parent_dir, 'luts', 'land', 'land_core_modis_terra.nc4')
            tcwv_op = cawa_land.CawaTcwvLandCore(land_lut)

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