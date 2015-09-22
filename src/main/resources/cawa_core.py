import os
import json
import functools
import tempfile
import copy
import wadamo_interpolators  # todo: we need mechanism to make these available in Calvalus environment!!
import wadamo_poly

import numpy as np
import cawa_utils as cu

######################################################################################
# The CAWA core operations (i.e. LUT access) for total water vapour column retrieval.
# Provided by FUB (RP), June 2014
######################################################################################
import time
import sys


def j2d(jsfile,exclude=[],order=None):
        with open(jsfile,"r") as fp:
          out=json.load(fp)

        def transform_list_to_np(tmp,order=order):
          for key in tmp:
            if isinstance(tmp[key],list) and (key not in exclude):
              try:
                    tmp[key]=np.array(tmp[key],order=order)
              except ValueError:
                    #print key,'geht nicht'
                    pass
            elif isinstance(tmp[key],dict):
              #recursion is save, since json has no circles
              transform_list_to_np(tmp[key],order=order)
          return tmp

        return transform_list_to_np(out,order=order)


cachedir = os.path.join(tempfile.gettempdir(),'wadaomo')
from joblib import Memory
memory = Memory(cachedir=cachedir, verbose=1)
memcached_j2d=memory.cache(j2d)


class cawa_core:
    '''
    ee
    '''
    def __init__(self,corefile=os.path.join('luts','wadamo_core_meris.json')):
        '''
        dgfra
        '''
        self.cawa_utils = cu.cawa_utils()
        self.num_computations = 0

        # 0 read LUT.
        #self.lut = d2j.json2dict(corefile,order='F')
        self.lut = memcached_j2d(corefile,order='F')
        self.wb  = self.lut['win_bnd'].tolist()
        self.ab  = self.lut['abs_bnd'].tolist()
        self.fb  = self.lut['fig_bnd'].tolist()
        self.prf = self.lut['ckd'][self.ab[0]].keys()
        self.prs = self.lut['ckd'][self.ab[0]][self.prf[0]]['prs']
        self.min_prs = self.prs.min()
        self.max_prs = self.prs.max()
        # self.about_me=about_me()

        self.nle = self.prs.shape[0]

        print('1. interpolators for 1d-dimensions ...')
        # 1. interpolators for 1d-dimensions
        t1 = time.clock() * 1000
        def make_1d_interpolators(xx):
            out={}
            for cha in xx:
                out[cha]={}
                for dim in xx[cha]['dimensions']:
                    out[cha][dim]=generate_interpol_to_index(xx[cha][dim])
            return out
        self.intp={}
        for lut in ('atc','scf_low','scf_hig'):
            self.intp[lut] = make_1d_interpolators(self.lut[lut])
        self.intp['prs'] = generate_interpol_to_index(self.prs)
        t2 = time.clock() * 1000
        print('init_1: ', (t2 - t1))

        # 2. All  watervapor-to-transmission operators
        t1 = time.clock() * 1000
        def make_transmission_operators(ch,poly=False):
            out={}
            for iprf in self.prf:
                dam=[]
                for iprs in range(self.nle):
                    if poly:
                        par=np.array(self.lut['ckd'][ch][iprf]['wvc2trn_coeff'][iprs,:],order='F')
                        dam.append(lambda x,a,par=par: wrap_wvc2trn_pol1(x*a,par))
                    else:
                        nor = self.lut['ckd'][ch][iprf]['tcwv'][iprs]
                        tau = self.lut['ckd'][ch][iprf]['tau'][0:iprs+1,:].sum(axis=0)
                        wgt = self.lut['ckd'][ch][iprf]['wgt']
                        dam.append(lambda x,a,nor=nor,tau=tau,wgt=wgt:((np.exp(-tau*x*a/nor)*wgt).sum()).clip(0.,1.))
                out[iprf]=dam
            return out

        self.single_tro_poly={cha:make_transmission_operators(cha,poly=True) for cha in self.wb+self.ab}
        self.single_tro_kdis={cha:make_transmission_operators(cha) for cha in self.wb+self.ab}
        t2 = time.clock() * 1000
        print('init_2: ', (t2 - t1))

        # 3. window bands to absorption bands interpolators
        # assuming that I always have two window bands
        t1 = time.clock() * 1000
        def abs_b_int(ch):
            www= (self.lut['cha'][ch]['cwvl'] - self.lut['cha'][self.wb[0]]['cwvl']) \
                 / (self.lut['cha'][self.wb[1]]['cwvl'] - self.lut['cha'][self.wb[0]]['cwvl'])
            return lambda x,www=www: x[0]+(x[1]-x[0])*www
        self.win_to_abs_interpolator={cha:abs_b_int(cha) for cha in self.ab}
        t2 = time.clock() * 1000
        print('init_3: ', (t2 - t1))

        # 4. interpolators (6d) for scattering factor derivatives
        t1 = time.clock() * 1000
        self.d_sf={lut:
                       {what :
                            {ch:
                                 generate_interpol_derivatives(
                                     self.lut[lut][ch][what],
                                     [self.lut[lut][ch][dd] for dd in self.lut[lut][ch]['dimensions']]
                                 )
                             for ch in self.ab}
                        for what in ('d_sf__dwvc','d_sf__daot','d_sf__dalb') }
                   for lut in ('scf_low','scf_hig') }
        t2 = time.clock() * 1000
        print('init_4: ', (t2 - t1))

    def estimator(self, input, classif_data, poly=True,bands=None,abscor=True):
        '''
        :param input:  dict containing all necessary input (see tests)
        :param poly:   if true polynomes are used instead of exponetial sums.
                       Expsums are far slower, but always valid. I have found now
                       eception by using polynoms yet
        :param bands:  list if strings, naming the absorption bands to be used.
                       Default None means that all bands described in LUT are used
                       (and expected)
        :param abscor: If true, absorption correction coefficients are used
                       (set it TRUE for MERIS and MODIS)
        :return:       a dict containing the input the TCWV and some
                       diagnostics, uncertainties ...
        '''

        t1 = time.clock() * 1000
        data=copy.deepcopy(input)
        t2 = time.clock() * 1000
        # print('copy.deepcopy(input): ', (t2 - t1))

        # exclude mask pixels from computation:
        pixel_mask = self.cawa_utils.calculate_pixel_mask(classif_data)
        valid = pixel_mask == 0
        if not valid:
            data['tcwv'] = -999.0 # todo: define no_data value
            data ['sig_tcwv'] = -999.0
        else:
            t1 = time.clock() * 1000
            self._init_full(data,poly=poly,bands=bands,abscor=abscor)
            t2 = time.clock() * 1000
            # print('init_full(data,poly=poly,bands=bands,abscor=abscor): ', (t2 - t1))
            t1 = time.clock() * 1000
            self._do_inversion(data)
            t2 = time.clock() * 1000
            # print('_do_inversion(data): ', (t2 - t1))
            t1 = time.clock() * 1000
            self._exit_data(data)
            t2 = time.clock() * 1000
            # print('_exit_data(data): ', (t2 - t1))

        return data

    def _init_data(self,data):
        '''
        just to ensure that every data is numpy 64 array with one Element
        and one  dimension
        '''
        def conv_it(inn):
            if isinstance(inn,list):
                out=np.array(inn)
            elif isinstance(inn,np.ndarray):
                if len(inn.shape) == 0:
                    out = np.array([inn])
                elif len(inn.shape) >1:
                    out=inn.squeeze()
                else:
                    # do nothing
                    out=inn
            else:
                out = np.array([inn])
            return out

    def _exit_data(self,data):
        '''
        just to ensure that every data is scalar number and no 1dim array
        '''
        def conv_it(inn):
            if isinstance(inn,np.ndarray):
                out=float(inn)  # must be a 1 element !
            else:
                out=inn
            return out

        for kk in data:
            if isinstance(data[kk],dict):
                for jj in data[kk]:
                    data[kk][jj]=conv_it(data[kk][jj])
            else:
                data[kk]=conv_it(data[kk])

    def _init_atmc(self, data):
        '''
        Initialize atmospheric correction LUTs:
            subset all luts and interpolates them
            to viewing geometry and aot
        '''

        #1. subset atmc for win channels
        self.atmc={}
        for cha in self.lut['atc']:
            wo_geo=[self.intp['atc'][cha][dim](data[dim]) for dim in ['azi','vie','suz']]
            wo_aot=self.intp['atc'][cha]['aot'](data['aot'][cha])
            #self.atmc[cha]=self._interpol_5to1(self.lut['atc'][cha]['ltoa'],wo_geo,wo_aot)
            self.atmc[cha]=wrap_interpol_5to1(self.lut['atc'][cha]['ltoa'],wo_geo,wo_aot)
        self.atmc_intp={}
        #2. make interpolators rtoa--> alb
        for cha in self.lut['atc']:
            self.atmc_intp[cha]=generate_interpol(self.atmc[cha],self.lut['atc'][cha]['alb'])

    def _init_scat(self, data):
        '''
        Initialize the scattering factor  LUTs:
            subset all luts and interpolates them
            to viewing geometry, aot and alb
        '''

        #1. subset scat for absorption channels
        self.scat={}
        for lut in ('scf_hig','scf_low'):
            self.scat[lut]={}
            for cha in self.lut[lut]:
                wo_geo = [self.intp[lut][cha][dd](data[dd]) for dd in ['azi','vie','suz']]
                wo_aol = np.array([self.intp[lut][cha][dd](data[dd][cha]) for dd in ['aot','alb']])
                self.scat[lut][cha]=wrap_interpol_6to1(self.lut[lut][cha]['scat_factor'],wo_geo,wo_aol)
                #self.scat[lut][cha]= self._interpol_6to1(self.lut[lut][cha]['scat_factor'],wo_geo,wo_aol)

        #2. make interpolators tcwv -->  scat_fac  'scattering factor operator'
        self.sfo={}
        for lut in self.scat:
            self.sfo[lut]={}
            for cha in self.scat[lut]:
                self.sfo[lut][cha]=generate_interpol(self.lut[lut][cha]['wvc'],self.scat[lut][cha])

        #3. the derivative of  scatering factor operators to wv
        def generate_d_sf__d_wv(cc,ll):
            def d_sf__d_wv(x):
                dum0 = self.sfo[ll][cc](np.array([0.9*x],order='F'))
                dum1 = self.sfo[ll][cc](np.array([x*1.1],order='F'))
                return (dum1-dum0)/(0.2*x)
            return d_sf__d_wv

        self.d_sf__d_wv={ll:{cc:generate_d_sf__d_wv(cc,ll) for cc in self.sfo[ll]} for ll in self.sfo}


    def _init_prs_tmp(self,data,poly=True,abscor=True):
        '''
        1. find
            a) sourounding pressure level (prs)
            b) sourounding temperatures (profiles)(prf)

        2. generates the interpolating transmisson functions
        3. index the derivative of th transmission function
        4. generates the interpolating first guess functions
        '''

        # 0.)calc amf
        data['amf']=1./np.cos(np.deg2rad(data['suz'])) + 1./np.cos(np.deg2rad(data['vie']))

        #prs_idx= np.interp(np.clip(data['prs'],self.min_prs,self.max_prs),self.prs,np.arange(self.nle))
        prs_idx=wadamo_interpolators.linint2index(data['prs'],self.prs)


        # 1a)  pressure weights (need 2):
        l_prs_idx = int(np.ceil(prs_idx))
        u_prs_idx = int(l_prs_idx-1)     #( one level above)
        l_prs_wgt = prs_idx - u_prs_idx
        u_prs_wgt = 1. - l_prs_wgt

        # 1b)  find sourounding temps profile
        lprf,ltmp=None,0
        uprf,utmp=None,1000
        for prf in self.prf:
            dum =  self.lut['ckd'][self.ab[0]][prf]['tmp'][l_prs_idx]*l_prs_wgt \
                  +self.lut['ckd'][self.ab[0]][prf]['tmp'][u_prs_idx]*u_prs_wgt
            if dum < data['tmp'] and dum > ltmp:
                ltmp=dum
                lprf=prf
            if dum > data['tmp'] and dum < utmp:
                utmp=dum
                uprf=prf

        if uprf is not None and lprf is not None:
            l_tmp_wgt=(utmp-data['tmp'])/(utmp-ltmp)
            u_tmp_wgt=1.-l_tmp_wgt
        elif uprf is not None and lprf is  None:
            u_tmp_wgt = 1.
            l_tmp_wgt = 0.
            lprf=self.prf[0]
        elif uprf is None and lprf is not None:
            u_tmp_wgt = 0.
            l_tmp_wgt = 1.
            uprf=self.prf[0]
        else:
            print 'strange temperature:',data['tmp']
            #ToDo raise something and exit !=0

        #2.  interpolating transoperator
        def generate_wv2tr(ch):
            #print 'cc',self.lut['cor'][ch]
            if poly is True:
                single_tro=self.single_tro_poly
            else:
                single_tro=self.single_tro_kdis
            if abscor is True:
                ###########TODO: REMOVE, just TESTING
                #self.lut['cor'][ch]=[1.,2.]
                #self.lut['cor'][ch]=[0.,1.]
                ###########TODO: REMOVE, just TESTING
                a,b = self.lut['cor'][ch]
                #print a,b
            else:
                a,b=0.,1.
            ab=np.array((a,b),order='F')
            def wv2tr(x):
                out = x*0.
                for iprf,wprf in [[uprf,u_tmp_wgt],[lprf,l_tmp_wgt]]:
                    for iprs,wprs in [[u_prs_idx,u_prs_wgt],[l_prs_idx,l_prs_wgt]]:
                        out+= single_tro[ch][iprf][iprs](x,data['amf'])*wprf*wprs
                return wadamo_poly.explog(out,ab)
            return wv2tr
        self.tro={ch:generate_wv2tr(ch) for ch in self.ab+self.wb}

        #3. indexing transmission derivative  d_trans__d_tcwv
        if l_tmp_wgt > u_tmp_wgt:
            mprf=lprf
        else:
            mprf=uprf
        if l_prs_wgt > u_prs_wgt:
            m_prs_idx=l_prs_idx
        else:
            m_prs_idx=u_prs_idx
        def generate_d_tr__d_wv(ch):
            def d_tr__d_wv(x):
                #dum  = self.single_tro_poly[ch][mprf][m_prs_idx](np.array((x*0.99,x*1.01)),data['amf'])
                dum0 = self.single_tro_poly[ch][mprf][m_prs_idx](np.array(x*0.99),data['amf'])
                dum1 = self.single_tro_poly[ch][mprf][m_prs_idx](np.array(x*1.01),data['amf'])
                return (dum1-dum0)/(0.02*x)
            return d_tr__d_wv
        self.d_tro={ch:generate_d_tr__d_wv(ch) for ch in self.ab}   #+self.wb

        #4.  interpolating first guess-orator
        def generate_tr2wv(ch):
            def tr2wv(x,amf=data['amf']):
                xx=np.array(np.log(x),order='F')
                out=0.
                for iprf,wprf in [[uprf,u_tmp_wgt],[lprf,l_tmp_wgt]]:
                    for iprs,wprs in [[u_prs_idx,u_prs_wgt],[l_prs_idx,l_prs_wgt]]:
                        par = np.array(self.lut['ckd'][ch][iprf]['trn2wvc_coeff'][iprs,:],order='F')
                        dum=wrap_trn2wvc_pol(xx,par)
                        #print 'dum',dum
                        out+= dum*wprf*wprs
                return out/amf
            return tr2wv
        self.fgu={ch:generate_tr2wv(ch) for ch in self.ab}

    def _init_forward(self,data,used_bands=None):
        '''
        Define the forward function and its derivative.
        Just for comodity
        '''
        if used_bands is None: used_bands = self.ab
        self.frwrd={}
        for sflut in self.sfo:
            def tro(wv,sflut=sflut):
                return np.array( [ self.tro[ch](wv) *self.sfo[sflut][ch](wv)
                                  for ch in used_bands])
                # return np.array( [ self.tro[ch](wv)*self.sfo[sflut][ch](wv)
                #                   for ch in used_bands])
            self.frwrd[sflut]=tro

        self.d_frwrd={}
        for sflut in self.d_sf__d_wv:
            def d_tro(wv,sflut=sflut):
                # product rule
                return np.array([ self.d_tro[ch](wv)*self.sfo[sflut][ch](wv)
                                + self.tro[ch](wv)*self.d_sf__d_wv[sflut][ch](wv)
                               for ch in used_bands])
                # return np.array([ self.d_tro[ch](wv)*self.sfo[sflut][ch](wv)
                #                for ch in used_bands])
            self.d_frwrd[sflut]=d_tro
        self.used_bands=used_bands

    def _init_full(self,data,poly=True,bands=None,abscor=True):
        '''
        changes data!!
        '''
        t1 = time.clock() * 1000
        self._init_data(data)
        t2 = time.clock() * 1000
        # print('   _init_data: ', (t2 - t1))
        t1 = time.clock() * 1000
        self._init_atmc(data)
        t2 = time.clock() * 1000
        # print('   _init_atmc: ', (t2 - t1))
        t1 = time.clock() * 1000
        self._init_prs_tmp(data,poly=poly,abscor=abscor) # 0.17ms
        t2 = time.clock() * 1000
        # print('   _init_prs_tmp: ', (t2 - t1))
        t1 = time.clock() * 1000
        self._do_first_guess(data)  #0.17ms
        t2 = time.clock() * 1000
        # print('   _do_first_guess: ', (t2 - t1))
        t1 = time.clock() * 1000
        self._do_atmc(data)     #0.27ms
        t2 = time.clock() * 1000
        # print('   _do_atmc: ', (t2 - t1))
        t1 = time.clock() * 1000
        self._init_scat(data)   #0.19mx
        t2 = time.clock() * 1000
        # print('   _init_scat: ', (t2 - t1))
        t1 = time.clock() * 1000
        self._init_forward(data,used_bands=bands)  #0 ms
        t2 = time.clock() * 1000
        # print('   _init_forward: ', (t2 - t1))

    def _do_atmc(self,data):
        '''
        changes data !!!!!!!!!
        needs first guess water vapor
        '''
        #0. trans based on first guess
        t1 = time.clock() * 1000
        data['trans_fg']={ch:self.tro[ch](data['fgu']) for ch in self.wb+self.ab}
        t2 = time.clock() * 1000
        # print('   trans_fg: ', (t2 - t1))

        # 1. water vapor transmission correction in window bands
        t1 = time.clock() * 1000
        data['rtoa_0']={ch:data['rtoa'][ch]/data['trans_fg'][ch] for ch in self.wb}
        t2 = time.clock() * 1000
        # print('   water vapor transmission: ', (t2 - t1))

        # 2. aerosol correction in window bands
        t1 = time.clock() * 1000
        data['alb']={ch:self.atmc_intp[ch](data['rtoa_0'][ch]) for ch in self.wb}
        t2 = time.clock() * 1000
        # print('   alb: ', (t2 - t1))

        # 3. interpolation to absorption band
        t1 = time.clock() * 1000
        for ch in self.ab:
            for what in ('alb','rtoa_0'):
                rrr=data[what][self.wb[0]],data[what][self.wb[1]]
                data[what][ch]=self.win_to_abs_interpolator[ch](rrr)

        t2 = time.clock() * 1000
        # print('   interpolation: ', (t2 - t1))


    def _do_first_guess(self,data):
        '''
        changes data !!!!!!!!!
        '''
        nitter = 1
        data['fgu']=8.
        for ii in range(nitter):
            # interpolated window band for first guess
            rr = (data['rtoa'][self.wb[0]]/self.tro[self.wb[0]](data['fgu']),
                  data['rtoa'][self.wb[1]]/self.tro[self.wb[1]](data['fgu']))
            #rr = (data['rtoa'][self.wb[0]],
            #      data['rtoa'][self.wb[1]])
            ri = self.win_to_abs_interpolator[self.fb[0]](rr)
            # transmission
            tra=data['rtoa'][self.fb[0]]/ri
            # the fgu polynom:
            data['fgu']=self.fgu[self.fb[0]](tra)

    def _do_inversion(self,data):
        data['tcwv']=data['fgu']
        # so ist es implementiert in Hannes's programm, , aber falsch
        # yy = np.array([
        #             data['rtoa'][bb]/(data['alb'][bb]/np.pi*np.cos(np.deg2rad(data['suz'])))
        #                for bb in self.used_bands
        #              ])
        #
        # So ist es richtig:
        yy = np.array([  data['rtoa'][bb]/data['rtoa_0'][bb]
                           for bb in self.used_bands
                     ])
#        def jac(x):
#            return self.d_frwrd['scf_low'](x)
        #speed up:
        # jacobian is aprox the jacobianm of the first guess
        def fun(x,yy=yy):
            return yy-self.frwrd['scf_low'](x)
        def jac(x,ret=self.d_frwrd['scf_low'](data['fgu'])):
            return ret

        xx=np.array(data['fgu'])
        #print yy.mean()
        sy=np.identity(len(self.used_bands))
        #syi=np.linalg.inv(sy)
        syi=sy
        wv, iitter, sig, conv= self._invert_generic(fun,jac,syi,xx)
        data['tcwv']=wv
        data['niter']=iitter
        data['convergence']=conv
        #TODO real uncertainty
        data ['sig_tcwv']=wv*0.05

    def _invert_generic(self,func,jaco,syi,xx,sai=None,xa=None):
        '''
         func          function to find the root
         jaco          function that returns the coresponding jacobians
         syi           inverse of measurement error covariance
         sai           inverse of the background error covarince
                       zero by default (= zero prior information)
         xx            first guess statevector, needs to be consistent with func
         xa            a proiri statevector, needs to be consistent with sai and xx

         The genaral equation is:
         dx = SX # (
                JT # SY^-1 # dy
                +
                SA^-1 # dx_a
                )
         with: SX the current state vector error co-variance
               J  the the Jacobian dy_i/dx_j
               SY the measurement error co-variance
               SA the prior error co-variance,SA^-1 its inverse
               dy the difference between measurement and forward
               dx_a the difference between current state and prior

         SX can be calculated:
               SX^-1 = (J^T # SY^-1  # J) + SA^-1
         this is written e.g. in equation 2.30 in C. Rodgers book
         (for the linear problem, but who cares)

         This equation simplifies enormous, if SA is infinite
         in other words: if I have no prior knowledge
         Then SA^-1 becomes zero:

         dx = SX # (
                J^T # SY^-1 # dy
                )
         with: SX the current state vector error co-variance
               SX^-1 = (J^T # SY^-1  # J)
        '''

        SIGMA=0.0005**2
        NITTER=3

        ff=func(xx) #; print 'f(xx)',func(xx),func(xx).shape,xx.shape
        #print 'xx',xx.shape
        jj=jaco(xx) #; print 'j(xx)',jj.shape
        #print 'jj', jj.shape
        sig=(ff**2).mean()
        doit=(sig >= SIGMA)
        iitter=0
        if doit:
                for iitter in range(1,NITTER+1):
                        #should be the  real linear algebra inverse  but x is only scalar
                        #sx=inv(self._atba(jj,syi))
                        #print jj.shape
                        #print 'syi',syi.shape
                        sx=1./atba(jj,syi)
                        #should be the  real linear algebra dot-product  but x is only scalar
                        #dx=dot(sx,dot(jj.T,dot(syi,ff))).squeeze()
                        dx=sx*np.dot(jj.T,np.dot(syi,ff))
                        #print 'dx',dx.shape,xx,np.dot(jj.T,np.dot(syi,ff)).shape,sx.shape,np.dot(sx.T,np.dot(jj.T,np.dot(syi,ff))).shape
                        xx=xx+dx.squeeze()
                        ff=func(xx)
                        sig=(ff**2).mean()
                        #print iitter,sig
                        weiter=(sig >SIGMA)
                        if weiter: #pass
                            jj=jaco(xx)
                        else: break
        return xx,iitter,sig,iitter < (NITTER-1)

def slow_time_step(u, dx, dy):
    """Takes a time step using straight forward Python loops."""

    nx, ny = u.shape
    dx2, dy2 = dx ** 2, dy ** 2
    dnr_inv = 0.5 / (dx2 + dy2)

    err = 0.0
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            tmp = u[i, j]
            u[i, j] = ((u[i - 1, j] + u[i + 1, j]) * dy2 +
                       (u[i, j - 1] + u[i, j + 1]) * dx2) * dnr_inv
            diff = u[i, j] - tmp
            err += diff * diff
            # if i == 2 and j == 3:
                # print 'u,tmp,diff,err = ', u[i, j], ',', tmp, ',', diff, ',',err

    return u, np.sqrt(err)


def numpy_time_step(u, dx, dy):
    dx2, dy2 = dx ** 2, dy ** 2
    dnr_inv = 0.5 / (dx2 + dy2)
    u_old = u.copy()
    # The actual iteration
    u[1:-1, 1:-1] = ((u[0:-2, 1:-1] + u[2:, 1:-1]) * dy2 +
                     (u[1:-1, 0:-2] + u[1:-1, 2:]) * dx2) * dnr_inv
    v = (u - u_old).flat
    return u, np.sqrt(np.dot(v, v))


def atba(a,b):
    # at_b_a is an acronym for
    # the AT#B#A product
    return np.dot(np.dot(a.T,b),a)
def wrap_trn2wvc_pol(x,par):
    return wadamo_poly.poly(x,par)
def wrap_wvc2trn_pol(x,par,pot=0.3333333333):
    return wadamo_poly.polyexp(x,par,pot)
def wrap_wvc2trn_pol1(x,par,pot=0.3333333333):
    return wadamo_poly.polyexp1(x,par,pot)
def wrap_interpol_6to1(lut,wo_geo,wo_aol):
    xx=np.array([wo_aol[0],wo_aol[1],wo_geo[0],wo_geo[1],wo_geo[2]],order='F')
    out=wadamo_interpolators.interpol_6to1(xx,lut)
    return out
def wrap_interpol_5to1(lut,wo_geo,wo_aot):
    xx=np.array([wo_aot,wo_geo[0],wo_geo[1],wo_geo[2]],order='F')
    out=wadamo_interpolators.interpol_5to1(xx,lut)
    return out
def wrap_interpol_6(lud,dims,wo):
    return wadamo_interpolators.interpol_6_full(wo,lud,dims[0],dims[1],dims[2],dims[3],dims[4],dims[5])

def generate_interpol_derivatives(lud,dims):
    return functools.partial(wrap_interpol_6,lud,dims)
def generate_interpol_to_index(xx):
    return lambda x, xx=np.array(xx,order='F'): wadamo_interpolators.linint2index(x,xx)
def generate_interpol(xx,yy):
    return lambda x, xx=np.array(xx,order='F'),yy=np.array(yy,order='F'): \
                                          wadamo_interpolators.interpol_1_full(x,yy,xx)

