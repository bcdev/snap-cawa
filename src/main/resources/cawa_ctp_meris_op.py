import snappy
from snappy import SystemUtils

import os
import zipfile
import numpy as np

import tempfile
import sys

import time

from netCDF4 import Dataset


CTP_NODATA_VALUE = -999.0


class CawaCtpMerisOp:
    """
    The CAWA GPF operator for total water vapour column retrieval.
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
        f = open(tempfile.gettempdir() + '/cava_ctp.log', 'w')

        f.write('Python module location: ' + __file__ + '\n')
        # print('Python module location: ' + __file__ + '\n')
        f.write('Python module location parent: ' + resource_root + '\n')

        # get source product:
        source_product = operator.getSourceProduct('sourceProduct')
        if not source_product:
            raise RuntimeError('No source product specified or product not found - cannot continue.')

        f.write('Start initialize: source product is' + source_product.getName() + '\n')
        print('Start initialize: source product is' + source_product.getName() + '\n')

        if os.path.isdir(resource_root):
            f.write('resource_root is dir ' + '\n')
            print('resource_root is dir ' + '\n')
            cloud_lut = os.path.join(resource_root, 'luts/cloud_core_meris.nc4')
            str_coeffs_lut = os.path.join(resource_root, 'luts/stray_coeff_potenz4.nc')
            ws_alb_lut = os.path.join(resource_root, 'luts/ws_alb_10_2005.nc')
            shared_libs_dir = resource_root
        else:
            f.write('extracting resources... ' + '\n')
            with zipfile.ZipFile(resource_root) as zf:
                auxpath = SystemUtils.getAuxDataPath()
                f.write('auxpath: ' + str(auxpath) + '\n')

                if not os.path.exists(os.path.join(str(auxpath), 'cawa/luts/cloud_core_meris.nc4')):
                    cloud_lut = zf.extract('luts/cloud_core_meris.nc4', os.path.join(str(auxpath), 'cawa'))
                    f.write('extracted LUT cloud: ' + cloud_lut + '\n')
                else:
                    cloud_lut = os.path.join(str(auxpath), 'cawa/luts/cloud_core_meris.nc4')
                    f.write('existing LUT cloud: ' + cloud_lut + '\n')

                if not os.path.exists(os.path.join(str(auxpath), 'cawa/luts/stray_coeff_potenz4.nc')):
                    str_coeffs_lut = zf.extract('luts/stray_coeff_potenz4.nc', os.path.join(str(auxpath), 'cawa'))
                    f.write('extracted stray_coeff: ' + str_coeffs_lut + '\n')
                else:
                    str_coeffs_lut = os.path.join(str(auxpath), 'cawa/luts/stray_coeff_potenz4.nc')
                    f.write('existing stray_coeff: ' + str_coeffs_lut + '\n')

                if not os.path.exists(os.path.join(str(auxpath), 'cawa/luts/ws_alb_10_2005.nc')):
                    ws_alb_lut = zf.extract('luts/ws_alb_10_2005.nc', os.path.join(str(auxpath), 'cawa'))
                    f.write('extracted ws_alb_10: ' + ws_alb_lut + '\n')
                else:
                    ws_alb_lut = os.path.join(str(auxpath), 'cawa/luts/ws_alb_10_2005.nc')
                    f.write('existing ws_alb_10: ' + ws_alb_lut + '\n')

                shared_libs_dir = tempfile.gettempdir()
                if not os.path.exists(shared_libs_dir + '/lib-python'):
                    lib_interpolator = zf.extract('lib-python/interpolators.so', shared_libs_dir)
                    lib_nd_interpolator = zf.extract('lib-python/nd_interpolator.so', shared_libs_dir)
                    lib_oec = zf.extract('lib-python/optimal_estimation_core.so', shared_libs_dir)
                else:
                    lib_interpolator = os.path.join(str(shared_libs_dir), 'lib-python/interpolators.so')
                    lib_nd_interpolator = os.path.join(str(shared_libs_dir), 'lib-python/nd_interpolator.so')
                    lib_oec = os.path.join(str(shared_libs_dir), 'lib-python/optimal_estimation_core.so')

        f.write('shared_libs_dir = %s' % (shared_libs_dir + '/lib-python') + '\n')
        sys.path.append(shared_libs_dir + '/lib-python')

        import cawa_ctp_meris_core as cawa_core
        import cawa_utils as cu
        self.cawa = cawa_core.CawaCtpMerisCore(cloud_lut)
        self.cawa_utils = cu.CawaUtils()

        width = source_product.getSceneRasterWidth()
        height = source_product.getSceneRasterHeight()
        f.write('Source product width, height = ...' + str(width) + ', ' + str(height) + '\n')

        # get source bands:
        self.rad_10_band = self.get_band(source_product, 'radiance_10') # reflectance is from Idepix product!
        self.rad_11_band = self.get_band(source_product, 'radiance_11')

        self.detector_index_band = self.get_band(source_product, 'detector_index')

        self.sza_band = self.get_band(source_product, 'sun_zenith')
        self.vza_band = self.get_band(source_product, 'view_zenith')
        self.saa_band = self.get_band(source_product, 'sun_azimuth')
        self.vaa_band = self.get_band(source_product, 'view_azimuth')

        self.lat_band = self.get_band(source_product, 'latitude')
        self.lon_band = self.get_band(source_product, 'longitude')
        self.alt_band = self.get_band(source_product, 'dem_alt')

        self.l1_flag_band = self.get_band(source_product, 'l1_flags')
        self.classif_band = None
        if cu.CawaUtils.band_exists('pixel_classif_flags', source_product.getBandNames()):
            self.classif_band = self.get_band(source_product, 'pixel_classif_flags')

        # setup target product:
        cawa_product = snappy.Product('pyCAWA', 'CAWA CTP', width, height)
        cawa_product.setDescription('CAWA CTP product')
        cawa_product.setStartTime(source_product.getStartTime())
        cawa_product.setEndTime(source_product.getEndTime())

        # setup target bands:
        self.ctp_band = cawa_product.addBand('ctp', snappy.ProductData.TYPE_FLOAT32)
        self.ctp_band.setNoDataValue(CTP_NODATA_VALUE)
        self.ctp_band.setNoDataValueUsed(True)
        self.ctp_band.setUnit('hPa')
        self.ctp_band.setDescription('Cloud Top Pressure')
        self.ctp_flags_band = cawa_product.addBand('ctp_flags', snappy.ProductData.TYPE_UINT8)
        self.ctp_flags_band.setUnit('dl')
        self.ctp_flags_band.setDescription('CTP flags band')

        # copy flag bands, tie points, geocoding:
        snappy.ProductUtils.copyFlagBands(source_product, cawa_product, True)
        source_product.transferGeoCodingTo(cawa_product, None)

        with Dataset(str_coeffs_lut,'r') as stray_ncds:
            #get the full stray coeffs
            self.str_coeffs=np.array(stray_ncds.variables['STRAY'][:],order='F')
            self.lmd=np.array(stray_ncds.variables['LAMBDA'][:],order='F')

        doy = 28 # todo: get from input file name
        with Dataset(ws_alb_lut,'r') as wsalb_ncds:
            #get the full stray coeffs
            #get closest day of year
            doy_idx=np.abs(wsalb_ncds.variables['time'][:]-doy).argmin()
            self.alb = wsalb_ncds.variables['albedo'][doy_idx,:,:]

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

        rad_10_tile = operator.getSourceTile(self.rad_10_band, target_rectangle)
        rad_11_tile = operator.getSourceTile(self.rad_11_band, target_rectangle)

        detector_index_tile = operator.getSourceTile(self.rad_11_band, target_rectangle)

        rad_10_samples = rad_10_tile.getSamplesFloat()
        rad_11_samples = rad_11_tile.getSamplesFloat()

        detector_index_samples = detector_index_tile.getSamplesInt()

        rad_10_data = np.array(rad_10_samples, dtype=np.float32)
        rad_11_data = np.array(rad_11_samples, dtype=np.float32)

        rad_norm_10_data = rad_10_data/1255.4227 # solar flux band 10
        rad_norm_11_data = rad_11_data/1178.0286 # solar flux band 11

        detector_index_data = np.array(detector_index_samples, dtype=np.int16)

        sza_tile = operator.getSourceTile(self.sza_band, target_rectangle)
        vza_tile = operator.getSourceTile(self.vza_band, target_rectangle)
        saa_tile = operator.getSourceTile(self.saa_band, target_rectangle)
        vaa_tile = operator.getSourceTile(self.vaa_band, target_rectangle)

        lat_tile = operator.getSourceTile(self.lat_band, target_rectangle)
        lon_tile = operator.getSourceTile(self.lon_band, target_rectangle)
        alt_tile = operator.getSourceTile(self.alt_band, target_rectangle)

        l1_flag_tile = operator.getSourceTile(self.l1_flag_band, target_rectangle)
        l1_flag_samples = l1_flag_tile.getSamplesInt()
        l1_flag_data = np.array(l1_flag_samples, dtype=np.int16)

        sza_samples = sza_tile.getSamplesFloat()
        vza_samples = vza_tile.getSamplesFloat()
        saa_samples = saa_tile.getSamplesFloat()
        vaa_samples = vaa_tile.getSamplesFloat()

        lat_samples = lat_tile.getSamplesFloat()
        lon_samples = lon_tile.getSamplesFloat()
        alt_samples = alt_tile.getSamplesFloat()

        sza_data = np.array(sza_samples, dtype=np.float32)
        vza_data = np.array(vza_samples, dtype=np.float32)
        saa_data = np.array(saa_samples, dtype=np.float32)
        vaa_data = np.array(vaa_samples, dtype=np.float32)

        lat_data = np.array(lat_samples, dtype=np.float32)
        lon_data = np.array(lon_samples, dtype=np.float32)
        alt_data = np.array(alt_samples, dtype=np.float32)

        lat_idx = np.round((90.0 - lat_data)*20).astype(np.int).clip(0,3599)
        lon_idx = np.round((180.0 + lon_data)*20).astype(np.int).clip(0,7199)

        # azi_data = cu.CawaUtils.azi2azid(saa_data, vaa_data)
        azi_data = self.cawa_utils.azi2azid(saa_data, vaa_data)
        # prs_data = cu.CawaUtils.height2press(alt_data)
        prs_data = self.cawa_utils.height2press(alt_data)

        classif_data = np.empty(sza_data.shape)
        classif_data.fill(2) # cloud
        if self.classif_band:
            classif_tile = operator.getSourceTile(self.classif_band, target_rectangle)
            classif_samples = classif_tile.getSamplesInt()
            classif_data = np.array(classif_samples, dtype=np.int32)

        # classif_tile = operator.getSourceTile(self.classif_band, target_rectangle)
        # classif_samples = classif_tile.getSamplesInt()
        # classif_data = np.array(classif_samples, dtype=np.int32)

        # loop over whole tile:
        print('start loop over tile...')
        ctp_data = np.empty(rad_norm_10_data.shape[0], dtype=np.float32)
        for i in range(0, rad_norm_10_data.shape[0]):
            rad_lam11 = self.lmd[detector_index_data[i]]
            rad_stray = self.str_coeffs[detector_index_data[i]] * rad_norm_10_data[i]
            rad_norm_11_data[i] += rad_stray

            # get closest albedo
            # nearest neighbour
            # quick and dirty surface albedo (RP):
            rad_alb10 = self.alb[lat_idx[i],lon_idx[i]].clip(0,1.)

            input = {'suz': sza_data[i],
                     'vie': vza_data[i],
                     'azi': azi_data[i],
                     'prs': prs_data[i],
                     'dwl': rad_lam11 - self.cawa.cawa_ctp.cha['11']['cwvl'],    # first abs-band
                     'alb': rad_alb10,
                     'rtoa': {'10': rad_norm_10_data[i],
                              '11': rad_norm_11_data[i]},
                     }
            ctp_data[i] = self.cawa.compute_pixel_meris(input, classif_data[i], l1_flag_data[i])['ctp']

        # fill target tiles:
        print('fill target tiles...')
        ctp_tile = target_tiles.get(self.ctp_band)
        ctp_flags_tile = target_tiles.get(self.ctp_flags_band)

        # set CTP flag:
        # todo: define appropriate low/high flag
        ctp_flags = ctp_data == CTP_NODATA_VALUE
        ctp_flags = ctp_flags.view(np.uint8)  # a bit faster

        # set samples:
        ctp_tile.setSamples(ctp_data)
        ctp_flags_tile.setSamples(ctp_flags)


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
