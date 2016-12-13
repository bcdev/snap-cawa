import snappy
from snappy import SystemUtils

import os
import zipfile
import numpy as np

import tempfile
import sys

import time


TCWV_NODATA_VALUE = -999.0


class CawaTcwvModisOp:
    """
    The CAWA GPF operator for total water vapour column retrieval from MODIS (Aqua).
    Authors: O.Danne, N.Fomferra, October 2015
    """

    def __init__(self):
        pass

    def initialize(self, operator):
        """
        GPF initialize method
        :param operator
        :return:
        """
        resource_root = os.path.dirname(__file__)
        # f = open(os.path.dirname(resource_root) + '/cava_tcwv.log', 'w')
        f = open(tempfile.gettempdir() + '/cava_tcwv_modis.log', 'w')

        f.write('Python module location: ' + __file__ + '\n')
        f.write('Python module location parent: ' + resource_root + '\n')

        # get source product:
        source_product = operator.getSourceProduct('sourceProduct')
        if not source_product:
            raise RuntimeError('No source product specified or product not found - cannot continue.')

        # f.write('Start initialize: source product is' + source_product.getFileLocation().getAbsolutePath() + '\n')
        f.write('Start initialize: source product is' + source_product.getName() + '\n')

        # get pixel classification from Idepix:
        # classif_product = operator.getSourceProduct('classifProduct')
        # if not classif_product:
        #     raise RuntimeError('No pixel classification product specified or product not found - cannot continue.')
        #
        # get parameters:
        self.temperature = operator.getParameter('temperature')  # todo: get temperature field from ERA-Interim
        self.pressure = operator.getParameter('pressure')  # todo: get pressure field from ERA-Interim
        self.prior_aot = operator.getParameter('prior_aot')  # todo: clarify if only one AOT is needed

        if os.path.isdir(resource_root):
            land_lut = os.path.join(resource_root, 'luts/land/land_core_modis_aqua.nc4')
            ocean_lut = os.path.join(resource_root, 'luts/ocean/ocean_core_modis_aqua.nc4')
            shared_libs_dir = resource_root
        else:
            with zipfile.ZipFile(resource_root) as zf:
                auxpath = SystemUtils.getAuxDataPath()
                f.write('auxpath: ' + str(auxpath) + '\n')
                lut_dir_to_extract = os.path.join(str(auxpath), 'cawa')
                # if not os.path.exists(lut_dir_to_extract):
                #     land_lut = zf.extract('luts/land/land_core_modis_aqua.nc4', lut_dir_to_extract)
                #     ocean_lut = zf.extract('luts/ocean/ocean_core_modis_aqua.nc4', lut_dir_to_extract)
                land_lut = zf.extract('luts/land/land_core_modis_aqua.nc4', lut_dir_to_extract)
                ocean_lut = zf.extract('luts/ocean/ocean_core_modis_aqua.nc4', lut_dir_to_extract)

                shared_libs_dir = tempfile.gettempdir()
                if not os.path.exists(shared_libs_dir + '/lib-python'):
                    zf.extract('lib-python/interpolators.so', shared_libs_dir)
                    zf.extract('lib-python/nd_interpolator.so', shared_libs_dir)
                    zf.extract('lib-python/optimal_estimation_core.so', shared_libs_dir)

        f.write('LUT land: ' + land_lut + '\n')
        f.write('LUT ocean: ' + ocean_lut + '\n')

        f.write('shared_libs_dir = %s' % (shared_libs_dir + '/lib-python') + '\n')
        sys.path.append(shared_libs_dir + '/lib-python')

        #time.sleep(600)

        import cawa_tcwv_core as cawa_core
        import cawa_utils as cu
        self.cawa = cawa_core.CawaTcwvCore(land_lut, ocean_lut)
        self.cawa_utils = cu.CawaUtils()

        width = source_product.getSceneRasterWidth()
        height = source_product.getSceneRasterHeight()
        f.write('Source product width, height = ...' + str(width) + ', ' + str(height) + '\n')

        # get source bands:
        self.rho_toa_2_band = self.get_band(source_product, 'EV_250_Aggr1km_RefSB_2') # RefSB is from Idepix product!
        self.rho_toa_5_band = self.get_band(source_product, 'EV_500_Aggr1km_RefSB_5') # RefSB is from Idepix product!
        self.rho_toa_17_band = self.get_band(source_product, 'EV_1KM_RefSB_17')
        self.rho_toa_18_band = self.get_band(source_product, 'EV_1KM_RefSB_18')
        self.rho_toa_19_band = self.get_band(source_product, 'EV_1KM_RefSB_19')

        self.sza_band = self.get_band(source_product, 'SolarZenith')
        self.vza_band = self.get_band(source_product, 'SensorZenith')
        self.saa_band = self.get_band(source_product, 'SolarAzimuth')
        self.vaa_band = self.get_band(source_product, 'SensorAzimuth')

        self.prior_t2m_band = None
        self.prior_msl_band = None
        self.prior_tcwv_band = None
        self.prior_wsp_band = None
        if cu.CawaUtils.band_exists('t2m', source_product.getBandNames()):
            self.prior_t2m_band = self.get_band(source_product, 't2m')
        if cu.CawaUtils.band_exists('msl', source_product.getBandNames()):
            self.prior_msl_band = self.get_band(source_product, 'msl')
        if cu.CawaUtils.band_exists('tcwv', source_product.getBandNames()):
            self.prior_tcwv_band = self.get_band(source_product, 'tcwv')
        if cu.CawaUtils.band_exists('ws', source_product.getBandNames()):
            self.prior_wsp_band = self.get_band(source_product, 'ws')

        self.classif_band = self.get_band(source_product, 'pixel_classif_flags')

        # setup target product:
        cawa_product = snappy.Product('pyCAWA', 'CAWA TCWV', width, height)
        cawa_product.setDescription('CAWA TCWV product')
        cawa_product.setStartTime(source_product.getStartTime())
        cawa_product.setEndTime(source_product.getEndTime())

        # setup target bands:
        self.tcwv_band = cawa_product.addBand('tcwv', snappy.ProductData.TYPE_FLOAT32)
        self.tcwv_band.setNoDataValue(TCWV_NODATA_VALUE)
        self.tcwv_band.setNoDataValueUsed(True)
        self.tcwv_band.setUnit('mm')
        self.tcwv_band.setDescription('Total column of water vapour')
        self.tcwv_flags_band = cawa_product.addBand('tcwv_flags', snappy.ProductData.TYPE_UINT8)
        self.tcwv_flags_band.setUnit('dl')
        self.tcwv_flags_band.setDescription('TCWV flags band')

        # copy flag bands, tie points, geocoding:
        snappy.ProductUtils.copyFlagBands(source_product, cawa_product, True)
        # snappy.ProductUtils.copyFlagBands(classif_product, cawa_product, True)
        # snappy.ProductUtils.copyTiePointGrids(source_product, cawa_product) # todo: wait for fix in SNAP
        source_product.transferGeoCodingTo(cawa_product, None)

        operator.setTargetProduct(cawa_product)

        f.write('end initialize.')
        f.close()

    def compute(self, operator, target_tiles, target_rectangle):
        """
        GPF compute method
        :param operator
        :param target_tiles
        :param target_rectangle
        :return:
        """

        print('enter compute: rectangle = ', target_rectangle.toString())
        # if target_rectangle.y == 0:
        #     f1 = open(tempfile.gettempdir() + '/cava_tcwv' + str(target_rectangle.x) + '_' + str(target_rectangle.y) + '.log', 'w')
        #     f1.write('enter compute: rectangle = ' + target_rectangle.toString() + '\n')

        rho_toa_2_tile = operator.getSourceTile(self.rho_toa_2_band, target_rectangle)
        rho_toa_5_tile = operator.getSourceTile(self.rho_toa_5_band, target_rectangle)
        rho_toa_17_tile = operator.getSourceTile(self.rho_toa_17_band, target_rectangle)
        rho_toa_18_tile = operator.getSourceTile(self.rho_toa_18_band, target_rectangle)
        rho_toa_19_tile = operator.getSourceTile(self.rho_toa_19_band, target_rectangle)

        rho_toa_2_samples = rho_toa_2_tile.getSamplesFloat()
        rho_toa_5_samples = rho_toa_5_tile.getSamplesFloat()
        rho_toa_17_samples = rho_toa_17_tile.getSamplesFloat()
        rho_toa_18_samples = rho_toa_18_tile.getSamplesFloat()
        rho_toa_19_samples = rho_toa_19_tile.getSamplesFloat()

        rho_toa_2_data = np.array(rho_toa_2_samples, dtype=np.float32)
        rho_toa_5_data = np.array(rho_toa_5_samples, dtype=np.float32)
        rho_toa_17_data = np.array(rho_toa_17_samples, dtype=np.float32)
        rho_toa_18_data = np.array(rho_toa_18_samples, dtype=np.float32)
        rho_toa_19_data = np.array(rho_toa_19_samples, dtype=np.float32)

        sza_tile = operator.getSourceTile(self.sza_band, target_rectangle)
        vza_tile = operator.getSourceTile(self.vza_band, target_rectangle)
        saa_tile = operator.getSourceTile(self.saa_band, target_rectangle)
        vaa_tile = operator.getSourceTile(self.vaa_band, target_rectangle)

        classif_tile = operator.getSourceTile(self.classif_band, target_rectangle)
        classif_samples = classif_tile.getSamplesInt()
        classif_data = np.array(classif_samples, dtype=np.int32)

        sza_samples = sza_tile.getSamplesFloat()
        vza_samples = vza_tile.getSamplesFloat()
        saa_samples = saa_tile.getSamplesFloat()
        vaa_samples = vaa_tile.getSamplesFloat()

        sza_data = np.array(sza_samples, dtype=np.float32)
        vza_data = np.array(vza_samples, dtype=np.float32)
        saa_data = np.array(saa_samples, dtype=np.float32)
        vaa_data = np.array(vaa_samples, dtype=np.float32)

        prior_t2m_data = np.empty(sza_data.shape)
        prior_t2m_data.fill(self.temperature)
        if self.prior_t2m_band:
            prior_t2m_tile = operator.getSourceTile(self.prior_t2m_band, target_rectangle)
            prior_t2m_samples = prior_t2m_tile.getSamplesFloat()
            prior_t2m_data = np.array(prior_t2m_samples, dtype=np.float32)

        prior_msl_data = np.empty(sza_data.shape)
        prior_msl_data.fill(self.pressure)
        if self.prior_msl_band:
            prior_msl_tile = operator.getSourceTile(self.prior_msl_band, target_rectangle)
            prior_msl_samples = prior_msl_tile.getSamplesFloat()
            prior_msl_data = np.array(prior_msl_samples, dtype=np.float32)

        prior_tcwv_data = np.empty(sza_data.shape)
        prior_tcwv_data.fill(30.0)
        if self.prior_tcwv_band:
            prior_tcwv_tile = operator.getSourceTile(self.prior_tcwv_band, target_rectangle)
            prior_tcwv_samples = prior_tcwv_tile.getSamplesFloat()
            prior_tcwv_data = np.array(prior_tcwv_samples, dtype=np.float32)

        prior_wsp_data = np.empty(sza_data.shape)
        prior_wsp_data.fill(7.5)
        if self.prior_wsp_band:
            prior_wsp_tile = operator.getSourceTile(self.prior_wsp_band, target_rectangle)
            prior_wsp_samples = prior_wsp_tile.getSamplesFloat()
            prior_wsp_data = np.array(prior_wsp_samples, dtype=np.float32)

        # loop over whole tile:
        print('start loop over tile...')
        tcwv_data = np.empty(rho_toa_2_data.shape[0], dtype=np.float32)
        for i in range(0, rho_toa_2_data.shape[0]):
            input = {'suz': sza_data[i], 'vie': vza_data[i], 'azi': 180. - abs(saa_data[i] - vaa_data[i]),
                     'amf': 1. / np.cos(sza_data[i] * np.pi / 180.) + 1. / np.cos(vza_data[i] * np.pi / 180.),
                     'prs': prior_msl_data[i]/100.0, 'aot': self.prior_aot, 'tmp': prior_t2m_data[i],
                     'rtoa': {'2': rho_toa_2_data[i]*np.cos(sza_data[i] * np.pi / 180.),
                              '5': rho_toa_5_data[i]*np.cos(sza_data[i] * np.pi / 180.),
                              '17': rho_toa_17_data[i]*np.cos(sza_data[i] * np.pi / 180.),
                              '18': rho_toa_18_data[i]*np.cos(sza_data[i] * np.pi / 180.),
                              '19': rho_toa_19_data[i]*np.cos(sza_data[i] * np.pi / 180.)},
                     'prior_wsp': prior_wsp_data[i], 'prior_aot': 0.15,
                     'prior_al0': 0.13, 'prior_al1': 0.13, 'prior_tcwv': prior_tcwv_data[i]}

            tcwv_data[i] = self.cawa.compute_pixel_modis(input, classif_data[i])['tcwv']

        # fill target tiles:
        print('fill target tiles...')
        tcwv_tile = target_tiles.get(self.tcwv_band)
        tcwv_flags_tile = target_tiles.get(self.tcwv_flags_band)

        # set TCWV flag:
        # todo: define appropriate low/high flag
        # tcwv_low = tcwv_data < 5.0
        # tcwv_high = tcwv_data > 10.0
        # tcwv_flags = tcwvLow + 2 * tcwvHigh
        tcwv_flags = tcwv_data == TCWV_NODATA_VALUE
        tcwv_flags = tcwv_flags.view(np.uint8)  # a bit faster

        # set samples:
        tcwv_tile.setSamples(tcwv_data)
        tcwv_flags_tile.setSamples(tcwv_flags)

        # if target_rectangle.y == 0:
        #     f1.close()

    def dispose(self, operator):
        """
        The GPF dispose method. Nothing to do here.
        :param operator:
        :return:
        """
        pass

    def get_band(self, input_product, band_name):
        """
        Gets band from input product by name
        :param input_product
        :param band_name
        :return:
        """
        band = input_product.getBand(band_name)
        if not band:
            band = input_product.getTiePointGrid(band_name)
            if not band:
                raise RuntimeError('Product has no band or tpg with name', band_name)
        return band
