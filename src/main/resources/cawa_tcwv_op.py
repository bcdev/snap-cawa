import snappy
from snappy import SystemUtils

import os
import zipfile
import numpy as np
import cawa_tcwv_core as cawa_core

TCWV_NODATA_VALUE = -999.0


class CawaTcwvOp:
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
        print('Python module location: ' + __file__)
        resource_root = os.path.dirname(__file__)
        print('Python module location parent: ' + resource_root)

        # get source product:
        source_product = operator.getSourceProduct('sourceProduct')
        if not source_product:
            raise RuntimeError('No source product specified or product not found - cannot continue.')

        print('Start initialize: source product is', source_product.getFileLocation().getAbsolutePath())

        # get pixel classification from Idepix:
        classif_product = operator.getSourceProduct('classifProduct')
        if not classif_product:
            raise RuntimeError('No pixel classification product specified or product not found - cannot continue.')

        # get parameters:
        self.temperature = operator.getParameter('temperature')  # todo: get temperature field from ERA-Interim
        self.pressure = operator.getParameter('pressure')        # todo: get pressure field from ERA-Interim
        self.aot13 = operator.getParameter('aot_13')             # todo: clarify if only one AOT is needed
        self.aot14 = operator.getParameter('aot_14')
        self.aot15 = operator.getParameter('aot_15')

        with zipfile.ZipFile(resource_root) as zf:
            auxpath = SystemUtils.getAuxDataPath()
            print('auxpath: ' + str(auxpath))
            land_lut = zf.extract('luts/land/land_core_meris.nc4', os.path.join(str(auxpath), 'cawa'))
            ocean_lut = zf.extract('luts/ocean/ocean_core_meris.nc4', os.path.join(str(auxpath), 'cawa'))
            print('LUT land: ' + land_lut)
            print('LUT ocean: ' + ocean_lut)

        self.cawa = cawa_core.CawaTcwvCore(land_lut, ocean_lut)

        width = source_product.getSceneRasterWidth()
        height = source_product.getSceneRasterHeight()
        print('Source product width, height = ...', width, height)

        # get source bands:
        self.rhoToa13Band = self.get_band(source_product, 'reflec_13')
        self.rhoToa14Band = self.get_band(source_product, 'reflec_14')
        self.rhoToa15Band = self.get_band(source_product, 'reflec_15')
        self.szaBand = self.get_band(source_product, 'sun_zenith')
        self.vzaBand = self.get_band(source_product, 'view_zenith')
        self.vaaBand = self.get_band(source_product, 'view_azimuth')

        self.l1_flag_band = self.get_band(source_product, 'l1_flags')
        self.classif_band = self.get_band(classif_product, 'cloud_classif_flags')

        # setup target product:
        cawa_product = snappy.Product('pyCAWA', 'CAWA TCWV', width, height)
        cawa_product.setDescription('CAWA TCWV product')
        cawa_product.setStartTime(source_product.getStartTime())
        cawa_product.setEndTime(source_product.getEndTime())

        # setup target bands:
        self.tcwvBand = cawa_product.addBand('tcwv', snappy.ProductData.TYPE_FLOAT32)
        self.tcwvBand .setNoDataValue(TCWV_NODATA_VALUE)
        self.tcwvBand .setNoDataValueUsed(True)
        self.tcwvBand .setUnit('mm')
        self.tcwvBand .setDescription('Total column of water vapour')
        self.tcwvFlagsBand = cawa_product.addBand('tcwv_flags', snappy.ProductData.TYPE_UINT8)
        self.tcwvFlagsBand .setUnit('dl')
        self.tcwvFlagsBand .setDescription('TCWV flags band')

        # copy flag bands, tie points, geocoding:
        snappy.ProductUtils.copyFlagBands(source_product, cawa_product, True)
        snappy.ProductUtils.copyFlagBands(classif_product, cawa_product, True)
        snappy.ProductUtils.copyTiePointGrids(source_product, cawa_product)
        source_product.transferGeoCodingTo(cawa_product, None)

        operator.setTargetProduct(cawa_product)

        print('end initialize.')

    def compute(self, operator, target_tiles, target_rectangle):
        """
        GPF compute method
        :param operator
        :param target_tiles
        :param target_rectangle
        :return:
        """

        print('enter compute: rectangle = ', target_rectangle.toString())

        rhoToa13Tile = operator.getSourceTile(self.rhoToa13Band, target_rectangle)
        rhoToa14Tile = operator.getSourceTile(self.rhoToa14Band, target_rectangle)
        rhoToa15Tile = operator.getSourceTile(self.rhoToa15Band, target_rectangle)

        rhoToa13Samples = rhoToa13Tile.getSamplesFloat()
        rhoToa14Samples = rhoToa14Tile.getSamplesFloat()
        rhoToa15Samples = rhoToa15Tile.getSamplesFloat()

        rhoToa13Data = np.array(rhoToa13Samples, dtype=np.float32)
        rhoToa14Data = np.array(rhoToa14Samples, dtype=np.float32)
        rhoToa15Data = np.array(rhoToa15Samples, dtype=np.float32)

        szaTile = operator.getSourceTile(self.szaBand, target_rectangle)
        vzaTile = operator.getSourceTile(self.vzaBand, target_rectangle)
        vaaTile = operator.getSourceTile(self.vaaBand, target_rectangle)

        l1_flag_tile = operator.getSourceTile(self.l1_flag_band, target_rectangle)
        l1_flag_samples = l1_flag_tile.getSamplesInt()
        l1_flag_data = np.array(l1_flag_samples, dtype=np.int16)

        classif_tile = operator.getSourceTile(self.classif_band, target_rectangle)
        classif_samples = classif_tile.getSamplesInt()
        classif_data = np.array(classif_samples, dtype=np.int32)

        szaSamples = szaTile.getSamplesFloat()
        vzaSamples = vzaTile.getSamplesFloat()
        vaaSamples = vaaTile.getSamplesFloat()

        szaData = np.array(szaSamples, dtype=np.float32)
        vzaData = np.array(vzaSamples, dtype=np.float32)
        vaaData = np.array(vaaSamples, dtype=np.float32)

        # loop over whole tile:
        print('start loop over tile...')
        tcwvData = np.empty(rhoToa13Data.shape[0], dtype=np.float32)
        for i in range(0, rhoToa13Data.shape[0]):
            input = {'suz': szaData[i], 'vie': vzaData[i], 'azi': vaaData[i],
                   'amf': 1. / np.cos(40. * np.pi / 180.) + 1. / np.cos(10. * np.pi / 180.),
                   'prs': self.pressure, 'aot': self.aot13, 'tmp': self.temperature,
                   'rtoa': {'13': rhoToa13Data[i], '14': rhoToa14Data[i], '15': rhoToa15Data[i]},
                   'prior_wsp':7.5,'prior_aot':0.15,
                   'prior_al0': 0.13, 'prior_al1': 0.13, 'prior_tcwv': 15.}

            tcwvData[i] = self.cawa.compute_pixel(input, classif_data[i], l1_flag_data[i])['tcwv']

        # fill target tiles:
        print('fill target tiles...')
        tcwvTile = target_tiles.get(self.tcwvBand)
        tcwvFlagsTile = target_tiles.get(self.tcwvFlagsBand)

        # set TCWV flag:
        # todo: define appropriate low/high flag
        # tcwvLow = tcwvData < 5.0
        # tcwvHigh = tcwvData > 10.0
        # tcwvFlags = tcwvLow + 2 * tcwvHigh
        tcwvFlags = tcwvData == TCWV_NODATA_VALUE
        tcwvFlags = tcwvFlags.view(np.uint8) # a bit faster

        #set samples:
        tcwvTile.setSamples(tcwvData)
        tcwvFlagsTile.setSamples(tcwvFlags)

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
