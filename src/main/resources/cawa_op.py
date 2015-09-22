import os
import zipfile

import numpy

import snappy
import sys
import cawa_core

import cawa_utils as cu

from joblib import Memory
from snappy import SystemUtils

jpy = snappy.jpy

LAT_VALID_MIN_VALUE = -90.0
LAT_VALID_MAX_VALUE = 90.0
LAT_NODATA_VALUE = -999.0
LON_VALID_MIN_VALUE = -180.0
LON_VALID_MAX_VALUE = 180.0
LON_NODATA_VALUE = -999.0

TCWV_NODATA_VALUE = -999.0

class CawaOp:

    def initialize(self, operator):
        source_product = operator.getSourceProduct('sourceProduct')
        if not source_product:
            raise RuntimeError('No source product specified or product not found - cannot continue.')

        print('start initialize: source product is', source_product.getFileLocation().getAbsolutePath())

        # pixel classification from Idepix:
        classif_product = operator.getSourceProduct('classifProduct')
        if not classif_product:
            raise RuntimeError('No pixel classification product specified or product not found - cannot continue.')

        print('Python module location: ' + __file__)
        resource_root = os.path.dirname(__file__)
        print('Python module location parent: ' + resource_root)

        print('get parameters ...')
        self.temperature = operator.getParameter('temperature')
        self.pressure = operator.getParameter('pressure')
        self.aot13 = operator.getParameter('aot_13')
        self.aot14 = operator.getParameter('aot_14')
        self.aot15 = operator.getParameter('aot_15')
        self.sig_aot13 = self.aot13
        self.sig_aot14 = self.aot14
        self.sig_aot15 = self.aot15

        self.cawa_utils = cu.cawa_utils()

        with zipfile.ZipFile(resource_root) as zf:
            auxpath = SystemUtils.getAuxDataPath()
            print('auxpath: ' + str(auxpath))
            lut_json = zf.extract('luts/wadamo_core_meris.json', os.path.join(str(auxpath), 'cawa'))
            self.cawa = cawa_core.cawa_core(lut_json)
            print('LUT json file: ' + lut_json)

        width = source_product.getSceneRasterWidth()
        height = source_product.getSceneRasterHeight()
        print('width, height = ...', width, height)

        print('get bands ...')
        # todo: add something similar for MODIS input
        self.rhoToa13Band = self.get_band(source_product, 'reflec_13')
        self.rhoToa14Band = self.get_band(source_product, 'reflec_14')
        self.rhoToa15Band = self.get_band(source_product, 'reflec_15')
        self.szaBand = self.get_band(source_product, 'sun_zenith')
        print('got band vza ...')
        self.vzaBand = self.get_band(source_product, 'view_zenith')
        self.vaaBand = self.get_band(source_product, 'view_azimuth')

        self.classif_band = self.get_band(classif_product, 'cloud_classif_flags')

        print('setup target product...')
        cawa_product = snappy.Product('pyCAWA', 'pyCAWA', width, height)
        cawa_product.setPreferredTileSize(width, 16)
        cawa_product.setPreferredTileSize(width, height)   # todo: wadamo_core does not yet support multi-threading with smaller tiles
        self.tcwvBand = cawa_product.addBand('tcwv', snappy.ProductData.TYPE_FLOAT32)
        self.tcwvBand .setNoDataValue(TCWV_NODATA_VALUE)
        self.tcwvBand .setNoDataValueUsed(True)
        # todo: flag band
        self.tcwvFlagsBand = cawa_product.addBand('tcwv_flags', snappy.ProductData.TYPE_UINT8)

        lat_ac_band = self.copy_src_band(source_product, cawa_product, 'corr_latitude')
        lat_ac_band .setNoDataValue(LAT_NODATA_VALUE)
        lat_ac_band .setNoDataValueUsed(True)
        lon_ac_band = self.copy_src_band(source_product, cawa_product, 'corr_longitude')
        lat_ac_band .setNoDataValue(LON_NODATA_VALUE)
        lon_ac_band .setNoDataValueUsed(True)
        sza_ac_band = self.copy_src_band(source_product, cawa_product, 'sun_zenith')
        vza_ac_band = self.copy_src_band(source_product, cawa_product, 'view_zenith')
        vaa_ac_band = self.copy_src_band(source_product, cawa_product, 'sun_azimuth')
        vaa_ac_band = self.copy_src_band(source_product, cawa_product, 'view_azimuth')
        altitude_ac_band = self.copy_src_band(source_product, cawa_product, 'altitude')
        snappy.ProductUtils.copyFlagBands(source_product, cawa_product, True)
        snappy.ProductUtils.copyFlagBands(classif_product, cawa_product, True)

        # copy geocoding:
        source_product.transferGeoCodingTo(cawa_product, None)

        print('set target product...')
        operator.setTargetProduct(cawa_product)

        print('end initialize.')


    def compute(self, operator, target_tiles, target_rectangle):

        print('enter compute: rectangle = ', target_rectangle.toString())
        rhoToa13Tile = operator.getSourceTile(self.rhoToa13Band, target_rectangle)
        rhoToa14Tile = operator.getSourceTile(self.rhoToa14Band, target_rectangle)
        rhoToa15Tile = operator.getSourceTile(self.rhoToa15Band, target_rectangle)

        print('get rhoToaSamples ...')
        rhoToa13Samples = rhoToa13Tile.getSamplesFloat()
        rhoToa14Samples = rhoToa14Tile.getSamplesFloat()
        rhoToa15Samples = rhoToa15Tile.getSamplesFloat()

        rhoToa13Data = numpy.array(rhoToa13Samples, dtype=numpy.float32)
        rhoToa14Data = numpy.array(rhoToa14Samples, dtype=numpy.float32)
        rhoToa15Data = numpy.array(rhoToa15Samples, dtype=numpy.float32)

        szaTile = operator.getSourceTile(self.szaBand, target_rectangle)
        vzaTile = operator.getSourceTile(self.vzaBand, target_rectangle)
        vaaTile = operator.getSourceTile(self.vaaBand, target_rectangle)

        classif_tile = operator.getSourceTile(self.classif_band, target_rectangle)
        classif_samples = classif_tile.getSamplesInt()
        classif_data = numpy.array(classif_samples, dtype=numpy.int32)

        print('get geometry Samples ...')
        szaSamples = szaTile.getSamplesFloat()
        vzaSamples = vzaTile.getSamplesFloat()
        vaaSamples = vaaTile.getSamplesFloat()

        szaData = numpy.array(szaSamples, dtype=numpy.float32)
        vzaData = numpy.array(vzaSamples, dtype=numpy.float32)
        vaaData = numpy.array(vaaSamples, dtype=numpy.float32)

        # loop over whole tile...
        print('start loop ...')
        print('rhoToa13Data.size[0]: ', rhoToa13Data.shape[0])
        tcwvData = numpy.empty(rhoToa13Data.shape[0], dtype=numpy.float32)
        for i in range(0, rhoToa13Data.shape[0]):
            input={'tmp':self.temperature
                ,'prs':self.pressure
                ,'suz':szaData[i]
                ,'vie':vzaData[i]
                ,'azi':vaaData[i]
                ,'aot': {'13':self.aot13
                , '14':self.aot14
                , '15':self.aot15
                    }
                ,'sig_aot': {'13':self.sig_aot13
                , '14':self.sig_aot14
                , '15':self.sig_aot15
                            }
                ,'rtoa':{'13':rhoToa13Data[i]
                , '14':rhoToa14Data[i]
                , '15':rhoToa15Data[i]
                        }
            }
            # tcwvData[i] = i*1.0
            tcwvData[i] = self.getTcwv(self.cawa, input, classif_data[i])
            # print('i, time in millisec: ', i, ' // ', int(round(time.time() * 1000)))

        # fill target tiles...
        print('fill target tiles...')
        tcwvTile = target_tiles.get(self.tcwvBand)
        tcwvFlagsTile = target_tiles.get(self.tcwvFlagsBand)

        # todo: define appropriate low/high flag
        tcwvLow = tcwvData < 5.0
        tcwvHigh = tcwvData > 10.0
        tcwvFlags = tcwvLow + 2 * tcwvHigh
        tcwvFlags = tcwvData == TCWV_NODATA_VALUE
        # tcwvFlags = tcwvFlags.astype(numpy.uint8, copy=False)
        tcwvFlags = tcwvFlags.view(numpy.uint8) # a bit faster

        print('set samples...')
        tcwvTile.setSamples(tcwvData)
        tcwvFlagsTile.setSamples(tcwvFlags)

    def get_band(self, input_product, band_name):
        band = input_product.getBand(band_name)
        if not band:
            band = input_product.getTiePointGrid(band_name)
            if not band:
                raise RuntimeError('Product has no band or tpg with name', band_name)
        return band

    def copy_src_band(self, input_product, target_product, band_name):
        src_band = self.get_band(input_product, band_name)
        target_band = target_product.addBand(band_name, src_band.getDataType())
        target_band.setSourceImage(src_band.getSourceImage())
        target_band.setScalingFactor(src_band.getScalingFactor())
        target_band.setScalingOffset(src_band.getScalingOffset())
        target_band.setDescription(src_band.getDescription())
        target_band.setUnit(src_band.getUnit())
        target_band.setNoDataValue(src_band.getNoDataValue())
        target_band.setNoDataValueUsed(src_band.isNoDataValueUsed())
        return target_band



    def getTcwv(self, wd_algo, input, classif_data):
        return wd_algo.estimator(input, classif_data)['tcwv']


    def dispose(self, operator):
        pass
