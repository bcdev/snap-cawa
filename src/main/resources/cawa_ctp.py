import os,sys
import time
import numpy as np
from netCDF4 import Dataset

libdir=os.path.join(os.path.abspath(os.path.dirname(__file__)),'libs')
#sys.path.append(libdir)
sys.path.insert(1,libdir)

import optimal_estimation as oe
import lut2func
import lut2jacobian_lut

def about_me():
    dct = {}
    dct['scriptname'] = __file__
    dct['scriptdir'] = os.path.realpath(os.path.abspath(os.path.split(dct['scriptname'])[0]))
    dct['cawadir'] = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
    versfile = os.path.join(dct['scriptdir'], 'current_version.txt')
    dct['version'] = file(versfile).readlines()[0][:-1]
    dct['cwd'] = os.path.abspath(os.getcwd())
    dct['date']=time.ctime()
    return dct

HIER = about_me()['scriptdir']
__author__ = 'rene'
__version__ = next(open(os.path.join(HIER,'current_version.txt'))).rstrip()
__version_info__ = tuple([int(num) for num in __version__.split('.')])

#apriori error covariance 1d
# defacto nothing is known before
SAcot=2.   # log_10 cot units
SActp=500   # hPa
SA=np.zeros((2,2),order='F')
SA[1,1]=SAcot**2
SA[0,0]=SActp**2


def pos_in_list(l,e):
    return [i for i,x in enumerate(l) if x == e]

class CawaCtpCore:
    def __init__(self,
                 cloud_lut=os.path.join('.', 'luts', 'cloud_core_meris.nc4'),
                 str_coeffs_lut=os.path.join('.', 'luts', 'stray_coeff_potenz4.nc'),
                 ws_alb_lut=os.path.join('.', 'luts', 'ws_alb_10_2005.nc'),
                 used_ab=None):
        with Dataset(cloud_lut,'r') as cloud_lut_ncds:
            #get the full cloud lut
            self.lut=np.array(cloud_lut_ncds.variables['lut'][:],order='F')
            self.jlut=np.array(cloud_lut_ncds.variables['jlut'][:],order='F')
            self.axes=tuple([np.array(cloud_lut_ncds.variables[a][:]) for a in cloud_lut_ncds.variables['lut'].dimensions[:-1]])
            self.jaxes=tuple([np.array(cloud_lut_ncds.variables[a][:]) for a in cloud_lut_ncds.variables['jlut'].dimensions[:-1]])
            self.ny_nx=np.array(cloud_lut_ncds.variables['jaco'][:])
            self.wb=cloud_lut_ncds.getncattr('win_bnd').split(',')
            self.ab=cloud_lut_ncds.getncattr('abs_bnd').split(',')
            self.cha={bb:
                          {kk:cloud_lut_ncds.groups['cha'].groups[bb].getncattr(kk)
                            for kk in ('bwvl','cwvl')} 
                      for bb in self.wb+self.ab}

            if used_ab is None:
                self.ab_idx=None
            else:
                self.ab=[used_ab,]
                self.ab_idx=pos_in_list(cloud_lut_ncds.getncattr('abs_bnd').split(','),used_ab)[0]

        with Dataset(str_coeffs_lut,'r') as stray_ncds:
            #get the full stray coeffs
            self.str_coeffs=np.array(stray_ncds.variables['STRAY'][:],order='F')
            self.lmd=np.array(stray_ncds.variables['LAMBDA'][:],order='F')

        with Dataset(ws_alb_lut,'r') as wsalb_ncds:
            #get the full stray coeffs
            #get closest day of year
            doy_idx=np.abs(wsalb_ncds.variables['time'][:]-doy).argmin()
            alb = wsalb_ncds.variables['albedo'][doy_idx,:,:]
            #get closest albedo
            #nearest neighbour
            rad['alb10']= alb[lat_idx,lon_idx].clip(0,1.)

        #generic forward 
        self._forward=lut2func.lut2func(self.lut,self.axes)
        #generic jacobian 
        self._jacobian=lut2jacobian_lut.jlut2func({'lut':self.jlut
                                                   ,'axes':self.jaxes
                                                   ,'ny':self.ny_nx[0]
                                                   ,'nx':self.ny_nx[1]})

        #global predefinition of input for speed reasons
        self.xaa=np.zeros(2)
        self.par=np.zeros(5)
        self.mes=np.zeros(len(self.wb)+len(self.ab))
        
        #local predefine inp for speed
        inp=np.zeros(7)
       
        def forward(woo,par):
            '''
            Input:
                woo: state (ctp,cot)
                par: parameter (alb, sza, vza, azd, dwvl)                    
                aot is aot at winband [0]
                wvc is sqrt of wvc
                
            Output:
                normalized radiances at winbands and  absbands
            '''    
            inp[:2],inp[2:]=woo,par
            if self.ab_idx is None:
                return self._forward(inp)
            else:
                return self._forward(inp)[((0,1+self.ab_idx),)]
                
        self.forward =forward
        def jforward(woo,geo):
            '''
            as forward, but returns jacobian
            output must be limited to the first three elements (the state and not the geometry)
            '''
            inp[:2],inp[2:]=woo,geo            
            if self.ab_idx is None:
                return self._jacobian(inp)[:,:2]
            else:
                return self._jacobian(inp)[(0,1+self.ab_idx),:2]
        
        self.jforward=jforward
 
        #min_state
        a=np.array([self.axes[i].min() for i in range(2)])
        #max_state
        b=np.array([self.axes[i].max() for i in range(2)])       
        self.inverter=oe.my_inverter(self.forward,a,b,jaco=self.jforward)
        
        #finaly preset SE
        sew=[0.0001 for i in self.wb]
        sea=[0.0001  for i in self.ab]
        self.SE=np.diag(sew+sea)

    def _do_inversion(self,data,sa=SA,se=None):
        
        if se is None: se=self.SE
        
        
        for ich,ch in enumerate(self.wb):
            self.mes[ich]=data['rtoa'][ch]
        for ich,ch in enumerate(self.ab):
            self.mes[len(self.wb)+ich]=-np.log(data['rtoa'][ch] /  data['rtoa'][self.wb[0]])
        self.par[0]= data['alb']    
        self.par[1]= data['suz']    
        self.par[2]= data['vie']    
        self.par[3]= data['azi']
        self.par[4]= data['dwl']
        #todo think about real apriori
        self.xaa[0]= 500.    
        self.xaa[1]= 1.   
        
        #print self.mes
        res=self.inverter(self.mes,fparams=self.par,jparams=self.par
                          ,se=se,sa=sa,xa=self.xaa,method=2,full='fast',maxiter=3)
        
        
        # DEBUG: comment out, if not needed!
        #data['sim']=self.forward(res.x,self.par)
        #data['mes']=self.mes
        
        data['res']=res
        data['ctp']=res.x[0]
        data['cot']=res.x[1]

    def estimator(self,inp,sa=SA,se=None):
        if se is None: se=self.SE
        #data=copy.deepcopy(inp)
        data=inp
        self._do_inversion(data,sa=sa,se=se)

        return data
        
        


# if __name__=='__main__':
#     import cloud_core
    #cc=cloud_core.cloud_core()
    #print cc.cha
    
    #print cc.forward([200,1.2],[0.1,20.,30.,170,0.2])
    #print cc.forward([900,1.2],[0.1,20.,30.,170,0.2])
    ##print cc.jforward([500,1.2],[0.1,20.,30.,170,0.2])

    #inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':0.2
        #,'rtoa':{'10':0.188,'11':0.1}}
    #print cc.estimator(inp)['res'].x
    #inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':-0.2
        #,'rtoa':{'10':0.188,'11':0.1}}
    #print cc.estimator(inp)['res'].x
    #for xxx in np.linspace(0.08,0.12,10):
        #inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':0.2
            #,'rtoa':{'10':0.188,'11':xxx}}
        #print xxx,cc.estimator(inp)['res'].x

    #for xxx in np.linspace(-1.,1.,20):
        #inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':xxx
            #,'rtoa':{'10':0.188,'11':0.0868965517241}}
        #print xxx,cc.estimator(inp)['res'].x
        

    #cc=cloud_core.cloud_core('luts/cloud_core_olci.nc4')
    
    #print cc.forward([200,1.2],[0.1,20.,30.,170,0.2])
    #print cc.forward([700,1.2],[0.1,20.,30.,170,0.2])
    ##print cc.jforward([500,1.2],[0.1,20.,30.,170,0.2])

    #inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':0.2
        #,'rtoa':{'12':0.188,'13':0.10,'14':0.13,'15':0.18}}
    #print cc.estimator(inp)['res'].x

    #inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':-0.2
        #,'rtoa':{'12':0.188,'13':0.10,'14':0.13,'15':0.18}}
    #print cc.estimator(inp)['res'].x

    # cc=cloud_core.cloud_core('luts/cloud_core_olci.nc4')
    # ccc=cloud_core.cloud_core('luts/cloud_core_olci.nc4',used_ab='14')
    # print cc.forward([200,1.2],[0.1,20.,30.,170,0.2])
    # print ccc.forward([200,1.2],[0.1,20.,30.,170,0.2])
    # print cc.jforward([200,1.2],[0.1,20.,30.,170,0.2])
    # print ccc.jforward([200,1.2],[0.1,20.,30.,170,0.2])
    # inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':-0.2
    #     ,'rtoa':{'12':0.188,'13':0.10,'14':0.13,'15':0.18}}
    # print cc.estimator(inp)['res'].x
    #inp={'suz':10.,'vie':40.,'azi':170.,'alb':0.1,'dwl':-0.2
        #,'rtoa':{'12':0.188,'14':0.13}}
    #print ccc.estimator(inp)['res'].x
