import numpy as np
import interpolators_fortran as interpolators
#import interpolators_pure_python as interpolators


def is_monotonically_increasing(v):
    for i, e in enumerate(v[1:],1):
        if e <= v[i-1]:
            return False
    return True

def is_monotonically_decreasing(v):
    for i, e in enumerate(v[1:],1):
        if e >= v[i-1]:
            return False
    return True

def generate_interpol_to_index(xx):
    return lambda x, xx=np.array(xx,order='F'): interpolators.linint2index(x,xx)
def generate_interpol_to_index_rev(xx):
    return lambda x, xx=-np.array(xx,order='F'): interpolators.linint2index(-x,xx)


def check_luts(luts,ndim):
    for ilut,lut in enumerate(luts):
        print 'checking Lut %i'%ilut
        _= interpolators.checklut(lut)
    
def check_axes(axes):
    for idim,dim in enumerate(axes):
        print 'checking Axes %i'%idim
        _=interpolators.checklut(dim)


def lut2func(luts,axes,verbose=False,check_nans=False):
    '''
    Is actually a wrapper around an n-dimensional linear interpolation
    from R^m --> R^n
    
    Input:
    
        lut : tupel of n  m-dimensional np-arrays
              or an m+1 dimensional np-array
        axes: tupel of m 1d-numpy arrays
        
        check nans works only on tuple luts!
        
    Returns a function    
    
    '''
    
    #1. check validity of input:
    if isinstance(luts,tuple):
        for ilut,lut in enumerate(luts):
            if not isinstance(lut,np.ndarray):
                print ilut,' element is not an Numpy ndarray'
                return None
        
        shap=luts[0].shape
        ndim=luts[0].ndim
            
        for ilut,lut in enumerate(luts):
            if shap != lut.shape:
                print ilut,' ndarray has not the shape of ' , shap 

        #generate interpolating function
        if check_nans is True:
            itps=[interpolators.generate_nan_itp(lut) for lut in luts]
        else:   
            itps=[interpolators.generate_itp(lut) for lut in luts]
                
    elif isinstance(luts,np.ndarray):
        shap=luts.shape[:-1]
        ndim=luts.ndim-1
        itps=interpolators.generate_itp_pn(luts)

        
    else:
        print 'Input is neither an tupel of ndarrays nor an ndarray'
        return None       
 
    if not isinstance(axes,tuple):
        print 'Axes is not a tuple' 
        return None

    if len(axes) <> ndim:
        print 'Number of elements of axes (%i)'%len(axes) 
        print 'is not equal the number of dimensions (%i)'%ndim
        return None
    

    #2. analyze axes
    #
    for idim,dim in enumerate(axes):
        if not isinstance(dim,np.ndarray): 
            print 'Axes %i is not an Numpy ndarray' % idim
            return None
        if not dim.ndim == 1:
            print 'Axes %i is not an 1D Numpy ndarray' % idim
            return None
        if len(dim) <> shap[idim]:
            print 'Axes %i does not agree with the shape of LUT' % idim
            print 'Axes %i has %i elements but LUT needs %i.' % (idim,len(dim),shap[idim])
            return None
 

    #3. generate axes 1d interpolators    
    axes_max=[]
    axes_min=[]
    axes_int=[]
    axes_imi=[]
    axes_imd=[]
    
    for idim,dim in enumerate(axes):
        axes_imi.append(is_monotonically_increasing(dim))
        axes_imd.append(is_monotonically_decreasing(dim))

        if not (axes_imi[-1] or axes_imd[-1]) :
            print 'Axes %i is neither monotonically increasing nor decreasing' % idim
            print dim
            print 'Re-organize your data!'
            return None
        
        if not axes_imi[-1]:
            #print 'inverting dimension'
            axes_int.append(generate_interpol_to_index_rev(dim))
            axes_max.append(dim[0])
            axes_min.append(dim[-1])
        else:
            axes_int.append(generate_interpol_to_index(dim))
            axes_max.append(dim[-1])
            axes_min.append(dim[0])

    
    if isinstance(itps,list):
        def function(wo):
            woo=np.array([axe(w) for axe,w in zip(axes_int,wo)],order='F')
            out=np.array([itp(woo) for itp in itps],order='F')
            return out
    else:
        def function(wo):
            woo=np.array([axe(w) for axe,w in zip(axes_int,wo)],order='F')
            out=itps(woo) 
            return out
    
    
    return function


    

if __name__=='__main__':
    from lut2func import lut2func
    
    #example for R^2-->R^3
    
    luta=np.arange(24,dtype=np.float).reshape(6,4,order='C')
    lutb=np.arange(24,dtype=np.float).reshape(6,4,order='F')**2
    lutc=np.sqrt(np.arange(24,dtype=np.float).reshape(6,4,order='F'))
    luts=(luta,lutb,lutc)
    xx=np.array([3.,4.,6.,7.,9.,15.])
    yy=np.array([1.,5.,10,15])[::-1]
    axes=(xx,yy)
    
    funca=lut2func(luts,axes)

    luts=np.array((luta,lutb,lutc)).transpose([1,2,0])
    funcb=lut2func(luts,axes)
    
    import time
    for ff in (funca,funcb):
        a=time.time()
        for i in range(1000):
            _=ff(np.array([3.5,11.]))
        print _,': %i us'%((time.time()-a)*1000)    
    
    




