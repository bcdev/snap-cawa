import os,sys
import time
import numpy as np
from netCDF4 import Dataset

libdir=os.path.join(os.path.abspath(os.path.dirname(__file__)),'libs')
sys.path.append(libdir)

import optimal_estimation as oe
import lut2func
import lut2jacobian_lut



# def about_me():
#     dct = {}
#     dct['scriptname'] = __file__
#     dct['scriptdir'] = os.path.realpath(os.path.abspath(os.path.split(dct['scriptname'])[0]))
#     dct['cawadir'] = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
#     versfile = os.path.join(dct['scriptdir'], 'current_version.txt')
#     dct['version'] = file(versfile).readlines()[0][:-1]
#     dct['cwd'] = os.path.abspath(os.getcwd())
#     dct['date']=time.ctime()
#     return dct

# HIER = about_me()['scriptdir']
__author__ = 'rene'
# __version__ = next(open(os.path.join(HIER,'current_version.txt'))).rstrip()
# __version_info__ = tuple([int(num) for num in __version__.split('.')])

#measurement error covariance
#apriori error covariance 1d
SAw=25.   # (m/s) **2
SAa=0.1   # (1) **2
SAt=8.    # (kg/m2) , nich **2, da ich in sqrt(tcwv) rechne
SA=np.zeros((3,3),order='F')
SA[0,0]=SAt
SA[1,1]=SAa
SA[2,2]=SAw



class cawa_tcwv_ocean_core:
    '''
    '''
    def __init__(self,ocean_lut=os.path.join('.', 'luts', 'ocean', 'ocean_core_meris.nc4')):
    # def __init__(self,corefile=os.path.join(about_me()['cawadir'],'luts','ocean','ocean_core_meris.nc4')):
    #def __init__(self,corefile='/tmp/ocean_core_meris.json'):
        '''
        dgfra
        '''

        with Dataset(ocean_lut,'r') as ncds:
            #get the full lut
            self.lut=np.array(ncds.variables['lut'][:],order='F')
            self.jlut=np.array(ncds.variables['jlut'][:],order='F')
            self.axes=tuple([np.array(ncds.variables[a][:]) for a in ncds.variables['lut'].dimensions[:-1]])
            self.jaxes=tuple([np.array(ncds.variables[a][:]) for a in ncds.variables['jlut'].dimensions[:-1]])
            self.ny_nx=np.array(ncds.variables['jaco'][:])
            self.wb=ncds.getncattr('win_bnd').split(',')
            self.ab=ncds.getncattr('abs_bnd').split(',')

            

        #generic forward 
        self._forward=lut2func.lut2func(self.lut,self.axes)
        #generic jacobian 
        self._jacobian=lut2jacobian_lut.jlut2func({'lut':self.jlut
                                                   ,'axes':self.jaxes
                                                   ,'ny':self.ny_nx[0]
                                                   ,'nx':self.ny_nx[1]})

        
        
        #global predefinition of input for speed reasons
        self.xaa=np.zeros(3)
        self.par=np.zeros(3)
        self.mes=np.zeros(len(self.wb)+len(self.ab))
        
        #local predefine inp for speed
        inp=np.zeros(6)
        
        def forward(woo,geo):
            '''
            Input:
                woo: state (wvc aot wsp)
                geo: azi vie suz                    
                aot is aot at winband [0]
                wvc is sqrt of wvc
                
            Output:
                normalized radiances at winbands
                -np.log(effective_transmission)/sqrt(amf) at absbands
                
                effective_transmission= L_toa/L_0
                with L_0 is normalized radiance without water vapor
                                
            '''
            inp[:3],inp[3:]=woo,geo
            return self._forward(inp)
        
        self.forward=forward

        def jforward(woo,geo):
            '''
            as forward, but returns jacobian
            output must be limited to the first three elements (the state and not the geometry)
            '''
            inp[:3],inp[3:]=woo,geo            
            return self._jacobian(inp)[:,:3]
        
        self.jforward=jforward
        
        #min_state
        a=np.array([self.axes[i].min() for i in range(3)])
        #max_state
        b=np.array([self.axes[i].max() for i in range(3)])       
        self.inverter=oe.my_inverter(self.forward,a,b,jaco=self.jforward)
        
        #finaly preset SE
        sew=[0.0001 for i in self.wb]
        sea=[0.001  for i in self.ab]
        self.SE=np.diag(sew+sea)

        
        
    def _do_inversion(self,data,sa=SA,se=None):
        
        if se is None: se=self.SE
        
        #data['amf']=1./np.cos(data['vie']*np.pi/180.)+1./np.cos(data['suz']*np.pi/180.)
        
        for ich,ch in enumerate(self.wb):
            self.mes[ich]=data['rtoa'][ch]
        for ich,ch in enumerate(self.ab):
            self.mes[len(self.wb)+ich]=-np.log(
                      data['rtoa'][ch] /
                      data['rtoa'][self.wb[-1]])/np.sqrt(data['amf'])
        self.par[0]= data['azi']    
        self.par[1]= data['vie']    
        self.par[2]= data['suz']    
        self.xaa[0]= np.sqrt(data['prior_tcwv'])    
        self.xaa[1]= data['prior_aot']    
        self.xaa[2]= data['prior_wsp']    
        res=self.inverter(self.mes,fparams=self.par,jparams=self.par
                          ,se=se,sa=sa,xa=self.xaa,method=2,full='fast',maxiter=3)
        
        
        # DEBUG: comment out, if not needed!
        #data['sim']=self.forward(res.x,self.par)
        #data['mes']=self.mes
        
        data['res']=res
        data['tcwv']=res.x[0]**2
        data['aot']=res.x[1]
        data['wsp']=res.x[2]
           
    def estimator(self,inp,sa=SA,se=None):
        if se is None: se=self.SE
        #data=copy.deepcopy(inp)
        data=inp
        self._do_inversion(data,sa=sa,se=se)

        return data
            
            
                
 
# if __name__=='__main__':
#     import cawa_tcwv_ocean_core
#     oc=cawa_tcwv_ocean_core.cawa_tcwv_ocean_core()
#
#     print oc.forward([4.5,0.15,8.],[170.,20.,30.])
#     print oc.jforward([4.5,0.15,8.],[170.,20.,30.])
#
#     xa=np.array([3.,0.1,7.])
#
#     SE=np.diag([0.0001,0.0001,0.001])
#
#     print oc.inverter([ 0.0045663,0.00440355,0.21067386]
#                       ,fparams=np.array([170.,20.,30.])
#                       ,jparams=np.array([170.,20.,30.])
#                       ,sa=SA,se=SE,xa=xa,method=2,full=True,maxiter=4)
#
#     inp={'suz':10.,'vie':40.,'azi':170.,'amf':1./np.cos(40.*np.pi/180.)+1./np.cos(10.*np.pi/180.)
#         ,'rtoa':{'13':0.0045663,'14':0.00440355,'15':0.00356704375818}
#         ,'prior_wsp':7.5,'prior_aot':0.15,'prior_tcwv':15.}
#
#     print oc.estimator(inp)['res'].x
#
#     import time
#     tt=time.time
#     a=tt()
#     for i in range(1000): _=oc.forward([4.5,0.15,8.],[170.,20.,30.])
#     print 'forward',tt()-a
#     a=tt()
#     for i in range(1000): _=oc.inverter([ 0.0045663,0.00440355,0.21067386]
#                       ,fparams=np.array([170.,20.,30.])
#                       ,jparams=np.array([170.,20.,30.])
#                       ,sa=SA,se=SE,xa=xa,method=2,full=False,maxiter=4)
#     print 'inverter',tt()-a
#     a=tt()
#     for i in range(1000): _=oc.estimator(inp)['res'].x
#     print 'estimator',tt()-a
#
#     print HIER

