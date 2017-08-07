import snappy
from snappy import SystemUtils

import os
import zipfile
import numpy as np

import tempfile
import sys

for a in sys.path:
    print(a)

from netCDF4 import Dataset


CTP_NODATA_VALUE = -999.0


class CawaCtpOlciOp:
    """
    The CAWA GPF operator for total water vapour column retrieval (OLCI).
    Authors: O.Danne, N.Fomferra, October 2017
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

        f.write('Start initialize: source product is ' + source_product.getName() + '\n')
        print('Start initialize: source product is ' + source_product.getName() + '\n')

        if os.path.isdir(resource_root):
            f.write('resource_root is dir ' + '\n')
            print('resource_root is dir ' + '\n')
            cloud_lut = os.path.join(resource_root, 'luts/cloud_core_olci.nc4')
            str_coeffs_lut = os.path.join(resource_root, 'luts/stray_coeff_potenz4.nc')
            ws_alb_lut = os.path.join(resource_root, 'luts/ws_alb_10_2005.nc')
            spectral_fluxes_input_path = os.path.join(resource_root, 'luts/meris_sun_spectral_flux_rr_10_11.txt')
            shared_libs_dir = resource_root
        else:
            f.write('extracting resources... ' + '\n')
            with zipfile.ZipFile(resource_root) as zf:
                auxpath = SystemUtils.getAuxDataPath()
                f.write('auxpath: ' + str(auxpath) + '\n')

                if not os.path.exists(os.path.join(str(auxpath), 'cawa/luts/cloud_core_olci.nc4')):
                    cloud_lut = zf.extract('luts/cloud_core_olci.nc4', os.path.join(str(auxpath), 'cawa'))
                    f.write('extracted LUT cloud: ' + cloud_lut + '\n')
                else:
                    cloud_lut = os.path.join(str(auxpath), 'cawa/luts/cloud_core_olci.nc4')
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

                if not os.path.exists(os.path.join(str(auxpath), 'cawa/luts/meris_sun_spectral_flux_rr_10_11.txt')):
                    spectral_fluxes_input_path = zf.extract('luts/meris_sun_spectral_flux_rr_10_11.txt', os.path.join(str(auxpath), 'cawa'))
                    f.write('extracted meris_sun_spectral_flux_rr_10_11: ' + spectral_fluxes_input_path + '\n')
                else:
                    spectral_fluxes_input_path = os.path.join(str(auxpath), 'cawa/luts/meris_sun_spectral_flux_rr_10_11.txt')
                    f.write('existing meris_sun_spectral_flux_rr_10_11: ' + spectral_fluxes_input_path + '\n')

                shared_libs_dir = tempfile.gettempdir()
                # todo: add Windows case here
                if not os.path.exists(shared_libs_dir + '/lib-python'):
                    zf.extract('lib-python/interpolators.so', shared_libs_dir)
                    zf.extract('lib-python/nd_interpolator.so', shared_libs_dir)
                    zf.extract('lib-python/optimal_estimation_core.so', shared_libs_dir)
                else:
                    os.path.join(str(shared_libs_dir), 'lib-python/interpolators.so')
                    os.path.join(str(shared_libs_dir), 'lib-python/nd_interpolator.so')
                    os.path.join(str(shared_libs_dir), 'lib-python/optimal_estimation_core.so')

        f.write('shared_libs_dir = %s' % (shared_libs_dir + '/lib-python') + '\n')
        print 'shared_libs_dir: ', shared_libs_dir
        sys.path.append(shared_libs_dir + '/lib-python')

        import cawa_ctp_olci_core as cawa_core
        import cawa_utils as cu
        self.cawa = cawa_core.CawaCtpOlciCore(cloud_lut)
        self.cawa_utils = cu.CawaUtils()

        width = source_product.getSceneRasterWidth()
        height = source_product.getSceneRasterHeight()
        f.write('Source product width, height = ...' + str(width) + ', ' + str(height) + '\n')

        # get source bands:
        self.rad_12_band = self.get_band(source_product, 'Oa12_radiance')
        self.rad_13_band = self.get_band(source_product, 'Oa13_radiance')
        self.rad_14_band = self.get_band(source_product, 'Oa14_radiance')
        self.rad_15_band = self.get_band(source_product, 'Oa15_radiance')

        self.solar_flux_12_band = self.get_band(source_product, 'solar_flux_band_12')
        self.solar_flux_13_band = self.get_band(source_product, 'solar_flux_band_13')
        self.solar_flux_14_band = self.get_band(source_product, 'solar_flux_band_14')
        self.solar_flux_15_band = self.get_band(source_product, 'solar_flux_band_15')

        self.lambda0_13_band = self.get_band(source_product, 'lambda0_band_13')
        self.detector_index_band = self.get_band(source_product, 'detector_index')

        self.sza_band = self.get_band(source_product, 'SZA')
        self.vza_band = self.get_band(source_product, 'OZA')
        self.saa_band = self.get_band(source_product, 'SAA')
        self.vaa_band = self.get_band(source_product, 'OAA')

        self.lat_band = self.get_band(source_product, 'latitude')
        self.lon_band = self.get_band(source_product, 'longitude')
        self.alt_band = self.get_band(source_product, 'altitude')

        self.l1_flag_band = self.get_band(source_product, 'quality_flags')
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

        datestring = cu.CawaUtils.get_olci_product_datestring(source_product.getName())
        print('datestring: ' + datestring + '\n')
        doy = int(cu.CawaUtils.get_doy_from_yyyymmdd(datestring))
        print('doy: ' + str(doy) + '\n')

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

        rad_12_tile = operator.getSourceTile(self.rad_12_band, target_rectangle)
        rad_13_tile = operator.getSourceTile(self.rad_13_band, target_rectangle)
        rad_14_tile = operator.getSourceTile(self.rad_14_band, target_rectangle)
        rad_15_tile = operator.getSourceTile(self.rad_15_band, target_rectangle)

        solar_flux_12_tile = operator.getSourceTile(self.solar_flux_12_band, target_rectangle)
        solar_flux_13_tile = operator.getSourceTile(self.solar_flux_13_band, target_rectangle)
        solar_flux_14_tile = operator.getSourceTile(self.solar_flux_14_band, target_rectangle)
        solar_flux_15_tile = operator.getSourceTile(self.solar_flux_15_band, target_rectangle)

        lambda0_13_tile = operator.getSourceTile(self.lambda0_13_band, target_rectangle)
        detector_index_tile = operator.getSourceTile(self.detector_index_band, target_rectangle)

        rad_12_samples = rad_12_tile.getSamplesFloat()
        rad_13_samples = rad_13_tile.getSamplesFloat()
        rad_14_samples = rad_14_tile.getSamplesFloat()
        rad_15_samples = rad_15_tile.getSamplesFloat()

        solar_flux_12_samples = solar_flux_12_tile.getSamplesFloat()
        solar_flux_13_samples = solar_flux_13_tile.getSamplesFloat()
        solar_flux_14_samples = solar_flux_14_tile.getSamplesFloat()
        solar_flux_15_samples = solar_flux_15_tile.getSamplesFloat()

        lambda0_13_samples = lambda0_13_tile.getSamplesFloat()
        detector_index_samples = detector_index_tile.getSamplesInt()

        rad_12_data = np.array(rad_12_samples, dtype=np.float32)
        rad_13_data = np.array(rad_13_samples, dtype=np.float32)
        rad_14_data = np.array(rad_14_samples, dtype=np.float32)
        rad_15_data = np.array(rad_15_samples, dtype=np.float32)

        solar_flux_12_data = np.array(solar_flux_12_samples, dtype=np.float32)
        solar_flux_13_data = np.array(solar_flux_13_samples, dtype=np.float32)
        solar_flux_14_data = np.array(solar_flux_14_samples, dtype=np.float32)
        solar_flux_15_data = np.array(solar_flux_15_samples, dtype=np.float32)

        lambda0_13_data = np.array(lambda0_13_samples, dtype=np.float32)
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
        # prs_data = self.cawa_utils.height2press(alt_data) # not yet used

        classif_data = np.empty(sza_data.shape)
        classif_data.fill(2) # cloud
        if self.classif_band:
            classif_tile = operator.getSourceTile(self.classif_band, target_rectangle)
            classif_samples = classif_tile.getSamplesInt()
            classif_data = np.array(classif_samples, dtype=np.int32)

        # loop over whole tile:
        print('start loop over tile...')
        ctp_data = np.empty(rad_12_data.shape[0], dtype=np.float32)
        for i in range(0, rad_12_data.shape[0]):
            rad_norm_12 = rad_12_data[i]/solar_flux_12_data[i]
            rad_norm_13 = rad_13_data[i]/solar_flux_13_data[i]
            rad_norm_14 = rad_14_data[i]/solar_flux_14_data[i]
            rad_norm_15 = rad_15_data[i]/solar_flux_15_data[i]

            rad_lam13 = lambda0_13_data[i]

            # get closest albedo
            # nearest neighbour
            # quick and dirty surface albedo (RP):
            rad_alb10 = self.alb[lat_idx[i],lon_idx[i]].clip(0,1.)

            input = {'suz': sza_data[i],
                     'vie': vza_data[i],
                     'azi': azi_data[i],
                     'dwl': rad_lam13 - self.cawa.cawa_ctp.cha['13']['cwvl'],    # first abs-band
                     'alb': rad_alb10,
                     'rtoa': {'12': rad_norm_12,
                              '13': rad_norm_13,
                              '14': rad_norm_14,
                              '15': rad_norm_15}
                     }
            # print('input: ', input)
            ctp_data[i] = self.cawa.compute_pixel_ctp_olci(input, classif_data[i])['ctp']
            # print('ctp_data[i]: ', ctp_data[i])

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
