import interpolators as interpolators
# import nd_interpolator as nd_interpolator
import numpy as np

linint2index=interpolators.linint2index

def checklut(x):
    if not isinstance(x,np.ndarray) : print 'not numpy array',type(x)
    if x.ndim >=2 : 
        if not np.isfortran(x):
            print 'not in fortran order',x.flags
    if x.dtype != np.float64: print 'not float64'


def generate_itp(lut):
    ndim=lut.ndim
    
    if ndim == 1: interpolator = interpolators.interpol_1
    elif ndim == 2: interpolator = interpolators.interpol_2
    elif ndim == 3: interpolator = interpolators.interpol_3
    elif ndim == 4: interpolator = interpolators.interpol_4
    elif ndim == 5: interpolator = interpolators.interpol_5
    elif ndim == 6: interpolator = interpolators.interpol_6
    elif ndim == 7: interpolator = interpolators.interpol_7
    elif ndim >= 8: interpolator = interpolators.interpol_n
    else:
        print 'Not implemented'
        return
    
    if ndim <= 7:
        if np.isfortran(lut): my_lut=lut.astype(float)
        else: my_lut=np.asfortranarray(lut.astype(float))        
        def function(wo): 
            return interpolator(wo,my_lut)
    else: 
        if np.isfortran(lut): flat_lut=lut.astype(float).ravel('C')
        else: flat_lut=lut.astype(float).T.ravel('F')
        shape=np.array(lut.shape)
        size=lut.size
        def function(wo):
            return interpolator(wo,flat_lut,shape)
    
    return function

def generate_nan_itp(lut):
    ndim=lut.ndim
    
    if ndim == 1: interpolator = interpolators.interpol_nan_1
    elif ndim == 2: interpolator = interpolators.interpol_nan_2
    elif ndim == 3: interpolator = interpolators.interpol_nan_3
    elif ndim == 4: interpolator = interpolators.interpol_nan_4
    elif ndim == 5: interpolator = interpolators.interpol_5
    elif ndim == 6: interpolator = interpolators.interpol_6
    elif ndim == 7: interpolator = interpolators.interpol_7
    elif ndim >= 8: interpolator = interpolators.interpol_n
    else:
        print 'Not implemented'
        return
    
    if ndim <= 7:
        if np.isfortran(lut): my_lut=lut.astype(float)
        else: my_lut=np.asfortranarray(lut.astype(float))        
        def function(wo): 
            return interpolator(wo,my_lut)
    else: 
        if np.isfortran(lut): flat_lut=lut.astype(float).ravel('C')
        else: flat_lut=lut.astype(float).T.ravel('F')
        shape=np.array(lut.shape)
        size=lut.size
        def function(wo):
            return interpolator(wo,flat_lut,shape)
    
    return function


    
def generate_itp_pn(lut):
    ndim=lut.ndim-1
    
    if ndim == 1: interpolator = interpolators.interpol_1pn
    elif ndim == 2: interpolator = interpolators.interpol_2pn
    elif ndim == 3: interpolator = interpolators.interpol_3pn
    elif ndim == 4: interpolator = interpolators.interpol_4pn
    elif ndim == 5: interpolator = interpolators.interpol_5pn
    elif ndim == 6: interpolator = interpolators.interpol_6pn
    elif ndim >= 7: interpolator = interpolators.interpol_npn
    else:
        print 'Not implemented'
        return
    
    if ndim <= 6:
        if np.isfortran(lut): my_lut=lut
        else: my_lut=np.asfortranarray(lut)        
        def function(wo): 
            return interpolator(wo,my_lut)
    else: 
        if np.isfortran(lut): 
            flat_lut=np.asfortranarray(lut.reshape((-1,lut.shape[-1]) ,order='C'))
        else: 
            flat_lut=np.asfortranarray(lut.reshape((-1,lut.shape[-1]), order='C'))
        shape=np.array(lut.shape)
        size=shape[:-1].prod()
        def function(wo):
            return interpolator(wo,flat_lut,shape[0:-1],shape[-1])
    
    return function
    
