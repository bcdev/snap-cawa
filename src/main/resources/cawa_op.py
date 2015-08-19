import os
import zipfile

import numpy

import snappy
import sys
# import cawa_core

import cawa_utils as cu

from joblib import Memory
from snappy import SystemUtils

jpy = snappy.jpy


class CawaOp:

    def initialize(self, operator):
        sourceProduct = operator.getSourceProduct('source')
        print('start initialize: source product is', sourceProduct.getFileLocation().getAbsolutePath())

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
            lut_json = zf.extract('luts/wadamo_core_meris.json', os.path.join(str(auxpath), 'cawa'))
            # self.wd = cawa_core.cawa_core(lut_json)
            print('LUT json file: ' + lut_json)

        python_root = 'C:\\Python27'
        platform = 'windows32'
        ftn_libs_path = os.path.join('shared_libs', platform)
        print('python_root: ' + python_root)
        with zipfile.ZipFile(resource_root) as zf:
            wadamo_poly = zf.extract('shared_libs/windows32/f2py/wadamo_poly.pyd', os.path.join(python_root, 'cawa'))
            print('wadamo_poly: ' + wadamo_poly)

        width = sourceProduct.getSceneRasterWidth()
        height = sourceProduct.getSceneRasterHeight()
        print('width, height = ...', width, height)

        print('get bands ...')
        # todo: add something similar for MODIS input
        self.rhoToa13Band = self.getBand(sourceProduct, 'reflec_13')
        self.rhoToa14Band = self.getBand(sourceProduct, 'reflec_14')
        self.rhoToa15Band = self.getBand(sourceProduct, 'reflec_15')
        self.szaBand = self.getBand(sourceProduct, 'sun_zenith')
        print('got band vza ...')
        self.vzaBand = self.getBand(sourceProduct, 'view_zenith')
        self.vaaBand = self.getBand(sourceProduct, 'view_azimuth')

        print('setup target product...')
        cawaProduct = snappy.Product('pyCAWA', 'pyCAWA', width, height)
        cawaProduct.setPreferredTileSize(width, 16)
        cawaProduct.setPreferredTileSize(width, height)   # todo: wadamo_core does not yet support multi-threading with smaller tiles
        self.tcwvBand = cawaProduct.addBand('tcwv', snappy.ProductData.TYPE_FLOAT32)
        self.tcwvFlagsBand = cawaProduct.addBand('tcwv_flags', snappy.ProductData.TYPE_UINT8)

        print('set target product...')
        operator.setTargetProduct(cawaProduct)

        print('end initialize.')


    def compute(self, operator, targetTiles, targetRectangle):

        print('enter compute: rectangle = ', targetRectangle.toString())
        rhoToa13Tile = operator.getSourceTile(self.rhoToa13Band, targetRectangle)
        rhoToa14Tile = operator.getSourceTile(self.rhoToa14Band, targetRectangle)
        rhoToa15Tile = operator.getSourceTile(self.rhoToa15Band, targetRectangle)

        print('get rhoToaSamples ...')
        rhoToa13Samples = rhoToa13Tile.getSamplesFloat()
        rhoToa14Samples = rhoToa14Tile.getSamplesFloat()
        rhoToa15Samples = rhoToa15Tile.getSamplesFloat()

        rhoToa13Data = numpy.array(rhoToa13Samples, dtype=numpy.float32)
        rhoToa14Data = numpy.array(rhoToa14Samples, dtype=numpy.float32)
        rhoToa15Data = numpy.array(rhoToa15Samples, dtype=numpy.float32)

        szaTile = operator.getSourceTile(self.szaBand, targetRectangle)
        vzaTile = operator.getSourceTile(self.vzaBand, targetRectangle)
        vaaTile = operator.getSourceTile(self.vaaBand, targetRectangle)

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
            tcwvData[i] = self.getTcwv(self.wd, input)
            # print('i, time in millisec: ', i, ' // ', int(round(time.time() * 1000)))

        # fill target tiles...
        print('fill target tiles...')
        tcwvTile = targetTiles.get(self.tcwvBand)
        tcwvFlagsTile = targetTiles.get(self.tcwvFlagsBand)

        # todo: define low/high flag
        tcwvLow = tcwvData < 0.0
        tcwvHigh = tcwvData > 15.0
        tcwvFlags = tcwvLow + 2 * tcwvHigh

        print('set samples...')
        tcwvTile.setSamples(tcwvData)
        tcwvFlagsTile.setSamples(tcwvFlags)


    def getBand(self, inputProduct, bandName):
        band = inputProduct.getBand(bandName)
        if not band:
            band = inputProduct.getTiePointGrid(bandName)
            if not band:
                raise RuntimeError('Product has no band or tpg with name', bandName)
        return band


    def getTcwv(self, wd_algo, input):
        print('entered getTcwv...')
        print('wd_algo.estimator = ' + str(wd_algo.estimator))
        return wd_algo.estimator(input)['tcwv']


    def dispose(self, operator):
        pass
