import os,sys
import time

import cawa_utils as cu
import cawa_ctp

class CawaCtpOlciCore:

    """
    The CAWA core class for ctp retrieval.
    Basically a wrapper which determines the valid mask and calls the algorithm
    """

    def __init__(self, cloud_lut=os.path.join('.', 'luts', 'cloud_core_olci.nc4')):
        self.cawa_ctp = cawa_ctp.CawaCtpCore(cloud_lut)
        self.cawa_utils = cu.CawaUtils()

    def compute_pixel_olci(self, input, classif_flag, l1_flag):
        """
        derive pixel mask and call algorithm accordingly
        :param input:  dict containing all necessary input (see tests)
        :param classif_flag: Idepix flag
        :param l1_flag: L1 flag
        :return: a dict containing the input the TCWV and its uncertainty
        """

        data = input

        # exclude mask pixels from computation:
        pixel_mask = cu.CawaUtils.calculate_olci_ctp_pixel_mask(classif_flag)
        # pixel_mask = 0 # todo
        valid = pixel_mask == 0
        if not valid:
            data['ctp'] = -999.0  # todo: define no_data value
            data['sig_ctp'] = -999.0
        else:
            data['ctp'] = self.cawa_ctp.estimator(data)['ctp'] # test!
            data['sig_ctp'] = data['ctp'] * 0.05  # todo

        return data

