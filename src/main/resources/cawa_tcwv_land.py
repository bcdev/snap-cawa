import os
import sys
import time

import numpy as np

from netCDF4 import Dataset

import optimal_estimation as oe
import lut2func
import lut2jacobian_lut

__author__ = 'rene'

# measurement error covariance
# apriori error covariance 1d
SAa1 = 1.  # (1) **2
SAa0 = 1.  # (1) **2
SAt = 20.  # (kg/m2) , nich **2, da ich in sqrt(tcwv) rechne
SA = np.zeros((3, 3), order='F')
SA[0, 0] = SAt
SA[1, 1] = SAa0
SA[2, 2] = SAa1


class CawaTcwvLandCore:
    """
    TCWV algorithm for land (new, more performant version, provided by RP 20151015)
    """

    def __init__(self, land_lut=os.path.join('.', 'luts', 'land', 'land_core_meris.nc4')):
        libdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libs')
        sys.path.append(libdir)

        with Dataset(land_lut, 'r') as ncds:
            # get the full lut
            self.lut = np.array(ncds.variables['lut'][:], order='F')
            self.jlut = np.array(ncds.variables['jlut'][:], order='F')
            self.axes = tuple([np.array(ncds.variables[a][:]) for a in ncds.variables['lut'].dimensions[:-1]])
            self.jaxes = tuple([np.array(ncds.variables[a][:]) for a in ncds.variables['jlut'].dimensions[:-1]])
            self.ny_nx = np.array(ncds.variables['jaco'][:])
            self.wb = ncds.getncattr('win_bnd').split(',')
            self.ab = ncds.getncattr('abs_bnd').split(',')

        # generic forward
        self._forward = lut2func.lut2func(self.lut, self.axes)
        # generic jacobian
        self._jacobian = lut2jacobian_lut.jlut2func({'lut': self.jlut,
                                                     'axes': self.jaxes,
                                                     'ny': self.ny_nx[0],
                                                     'nx': self.ny_nx[1]})

        # global predefinition of input for speed reasons
        self.xaa = np.zeros(3)
        self.par = np.zeros(6)
        self.mes = np.zeros(len(self.wb) + len(self.ab))

        # local predefine inp for speed
        inp = np.zeros(9)

        def forward(woo, geo):
            """
            Input:
                woo: state (wvc al0 al1)
                geo: aot,prs,tmp,azi,vie,suz                    
                al0 is albedo at winband [0]
                al1 is albedo at winband [1]
                aot is aeros optical thickness at winband [1]
                prs is surface pressure in hPa
                tmp is 2m temperature is K
                wvc is sqrt of wvc
                
            Output:
                normalized radiances at winbands
                -np.log(effective_transmission) at absbands
                
                effective_transmission= L_toa/L_0
                with L_0 is normalized radiance without water vapor
                                
            """

            inp[:3], inp[3:] = woo, geo
            return self._forward(inp)

        self.forward = forward

        def jforward(woo, geo):
            """
            as forward, but returns jacobian
            output must be limited to the first three elements (the state and not the geometry)
            """
            inp[:3], inp[3:] = woo, geo
            return self._jacobian(inp)[:, :3]

        self.jforward = jforward

        # min_state
        a = np.array([self.axes[i].min() for i in range(3)])
        # max_state
        b = np.array([self.axes[i].max() for i in range(3)])
        self.inverter = oe.my_inverter(self.forward, a, b, jaco=self.jforward)

        # finaly preset SE
        sew = [0.0001 for i in self.wb]
        sea = [0.001 for i in self.ab]
        self.SE = np.diag(sew + sea)

    def _do_inversion(self, data, sa=SA, se=None):
        if se is None:
            se = self.SE

        for ich, ch in enumerate(self.wb):
            self.mes[ich] = data['rtoa'][ch]
        for ich, ch in enumerate(self.ab):
            self.mes[len(self.wb) + ich] = -np.log(
                data['rtoa'][ch] /
                data['rtoa'][self.wb[-1]]) / np.sqrt(data['amf'])
        self.par[0] = data['aot']
        self.par[1] = data['prs']
        self.par[2] = data['tmp']
        self.par[3] = data['azi']
        self.par[4] = data['vie']
        self.par[5] = data['suz']
        self.xaa[0] = np.sqrt(data['prior_tcwv'])
        self.xaa[1] = data['prior_al0']
        self.xaa[2] = data['prior_al1']
        #print 'par: ', self.par

        res = self.inverter(self.mes, fparams=self.par, jparams=self.par, se=se, sa=sa, xa=self.xaa, method=2,
                            full='fast', maxiter=3)

        data['res'] = res
        data['tcwv'] = res.x[0] ** 2
        data['al0'] = res.x[1]
        data['al1'] = res.x[2]

    def estimator(self, inp, sa=SA, se=None):
        if se is None:
            se = self.SE

        data = inp
        self._do_inversion(data, sa=sa, se=se)

        return data
