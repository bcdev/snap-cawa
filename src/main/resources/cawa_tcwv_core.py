import os
import time

import cawa_utils as cu
import cawa_tcwv_land as cawa_land
import cawa_tcwv_ocean as cawa_ocean

class cawa_tcwv_core:
    '''
    # The CAWA core class for total water vapour column retrieval.
    # Basically a wrapper which determines the valid mask and land/water distinction
    # and calls the corresponding algorithm (updates for land and water provided by FUB (RP), October 2014
    '''

    def __init__(self, land_lut=os.path.join('.', 'luts', 'land', 'land_core_meris.nc4'),
                       ocean_lut=os.path.join('.', 'luts', 'ocean', 'ocean_core_meris.nc4')):
        # self.cawa_land = cawa_land.cawa_tcwv_land_core(os.path.join('.', 'luts', 'land', 'land_core_meris.nc4'))
        self.cawa_land = cawa_land.cawa_tcwv_land_core(land_lut)
        # self.cawa_ocean = cawa_ocean.cawa_tcwv_ocean_core(os.path.join('.', 'luts', 'ocean', 'ocean_core_meris.nc4'))
        self.cawa_ocean = cawa_ocean.cawa_tcwv_ocean_core(ocean_lut)
        self.cawa_utils = cu.cawa_utils()

    def compute_pixel(self, input, classif_data, l1_flag_data):
        '''
        derive pixel mask,identify land or water, and call algorithm accordingly
        :param input:  dict containing all necessary input (see tests)
        :param classif_data: Idepix flag
        :param l1_flag_data: L1 flag
        :return:       a dict containing the input the TCWV and some
                       diagnostics, uncertainties ...
        '''

        data=input

        # exclude mask pixels from computation:
        pixel_mask = self.cawa_utils.calculate_meris_pixel_mask(classif_data, l1_flag_data)
        valid = pixel_mask == 0
        if not valid:
            data['tcwv'] = -999.0 # todo: define no_data value
            data ['sig_tcwv'] = -999.0
        else:
            land_mask = self.cawa_utils.is_meris_land_pixel(classif_data)
            is_water = land_mask == 0
            if is_water:
                data['tcwv'] = self.cawa_ocean.estimator(data)['tcwv']
            else:
                data['tcwv'] = self.cawa_land.estimator(data)['tcwv']

            data ['sig_tcwv'] = data['tcwv']*0.05 # todo

        return data

