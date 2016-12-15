import os
import time

import cawa_utils as cu
import cawa_tcwv_land as cawa_land
import cawa_tcwv_ocean as cawa_ocean


class CawaTcwvMerisCore:
    """
    The CAWA core class for total water vapour column retrieval.
    Basically a wrapper which determines the valid mask and land/water distinction
    and calls the corresponding algorithm (updates for land and water provided by FUB (RP), October 2015)
    """

    def __init__(self, land_lut=os.path.join('.', 'luts', 'land', 'land_core_meris.nc4'),
                 ocean_lut=os.path.join('.', 'luts', 'ocean', 'ocean_core_meris.nc4')):
        self.cawa_land = cawa_land.CawaTcwvLandCore(land_lut)
        self.cawa_ocean = cawa_ocean.CawaTcwvOceanCore(ocean_lut)
        self.cawa_utils = cu.CawaUtils()

    def compute_pixel_meris(self, input, classif_flag, l1_flag):
        """
        derive pixel mask,identify land or water, and call algorithm accordingly
        :param input:  dict containing all necessary input (see tests)
        :param classif_flag: Idepix flag
        :param l1_flag: L1 flag
        :return: a dict containing the input the TCWV and its uncertainty
        """

        data = input

        # exclude mask pixels from computation:
        pixel_mask = cu.CawaUtils.calculate_meris_pixel_mask(classif_flag, l1_flag)

        valid = pixel_mask == 0
        if not valid:
            data['tcwv'] = -999.0  # todo: define no_data value
            data['sig_tcwv'] = -999.0
        else:
            land_mask = self.cawa_utils.is_land_pixel_meris(classif_flag)
            is_water = land_mask == 0
            # if is_water:
            #     data['tcwv'] = self.cawa_ocean.estimator(data)['tcwv']
            # else:
            #     data['tcwv'] = self.cawa_land.estimator(data)['tcwv']

            data['tcwv'] = self.cawa_ocean.estimator(data)['tcwv'] # test!
            data['sig_tcwv'] = data['tcwv'] * 0.05  # todo

        return data

