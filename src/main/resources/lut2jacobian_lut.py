#generates a lut of jacobians from a lut
import numpy as np
import lut2func as l2f
from netCDF4 import Dataset
import wln


def numerical_jacoby(a, b, x, fnc, nx, ny, delta=0.01):
    '''

    :param a:
    :param b:
    :param x:
    :param fnc:
    :param nx:
    :param ny:
    :param delta:
    :return: Jacobian of fnc
    '''
    # very coarse but sufficient for this excercise
    #dx = np.array((b - a) * delta)
    dx=(b - a) * delta
    jac = np.empty((ny, nx),order='F')  # zeilen zuerst, spalten spaeter!!!!!!!
    for ix in range(nx):
        dxm = x * 1.
        dxp = x * 1.
        dxm[ix] = (dxm[ix] - dx[ix]).clip(a[ix],b[ix])
        dxp[ix] = (dxp[ix] + dx[ix]).clip(a[ix],b[ix])
        if dxp[ix] == dxm[ix]: 
            jac[:,ix]=0.
        else:
            dyy = fnc(dxp) - fnc(dxm)
            jac[:,ix]= dyy/(dxp[ix] - dxm[ix])       
    return jac


def generate_jacobian_lut(luts,axes):
    '''
    generates a jacobian-lut at exactly the same 
    positions (axes points) as the original luts
    
    '''   
    func=l2f.lut2func(luts,axes)
    
    if isinstance(luts,tuple):
        ny = len(luts)
    elif isinstance(luts,np.ndarray):
        ny = luts.shape[-1]
    else:
        print 'Luts is  not of right type'
        return None
    nx=len(axes)
    dimi=np.array([len(ax) for ax in (axes)])
    dimj=[len(ax) for ax in (axes)]
    dimj.append(ny*nx)
    out = np.zeros(dimj)
 
    a=np.zeros(len(axes))
    b=np.zeros(len(axes))
    
    a=np.array([ax.min() for ax in axes])
    b=np.array([ax.max() for ax in axes])
    
    def njac(x):
        return numerical_jacoby(a, b, x, func, nx, ny, delta=0.01)
    
    print('Filling the jacobian ...')
    progress=wln.wln(dimi.prod(),'Progress',modulo=10000)
    for i in np.arange(dimi.prod()): 
        idx=np.unravel_index(i,dimi)
        wo = np.array([ax[i] for i,ax in zip(idx,axes)])
        out[idx]=njac(wo).ravel()
        progress.event()
    print('')
    print('Done')

    return {'lut':out,'ny':ny,'nx':nx,'axes':axes}

def lut2ncdf(jlut,nfile):
    '''
    stores the  jacobian-lut and auxillary data
    in a ncdf
    
    '''
    with Dataset(nfile, 'w', format='NETCDF4') as nco:
        dim_ids=[]
        for i,a in enumerate(jlut['axes']):
            dimname='jlut_dimension_%i'%i
            nco.createDimension(dimname,a.size)
            dim_ids.append(dimname)
            ncdum=nco.createVariable('axes_%i'%i,a.dtype,dim_ids[-1])
            ncdum[:]=a
        dimname='jlut_dimension_%i'%(i+1)
        nco.createDimension(dimname,jlut['ny']*jlut['nx'])
        dim_ids.append(dimname)
        ncdum=nco.createVariable('jlut',jlut['lut'].dtype,dim_ids)
        ncdum[:]=jlut['lut']
        nco.createDimension('jaco_dimension',2)
        ncdum=nco.createVariable('ny_nx',np.int,'jaco_dimension')
        ncdum[:]=np.array([jlut['ny'],jlut['nx']])
        
def ncdf2func(nfile):
    '''
    reads jlut ncdf and makes a func from it
    '''
    with Dataset(nfile, 'r', format='NETCDF4') as nco:        
        jdims=nco.variables['jlut'].dimensions
        
        axes=tuple([nco.variables['axes_%i'%i][:] for i in range(len(jdims[:-1]))])
        jlut=nco.variables['jlut'][:]
        nynx=nco.variables['ny_nx'][:]

    dum={'lut':jlut,'ny':nynx[0],'nx':nynx[1],'axes':axes}   
    return jlut2func(dum)

def jlut2func(dum):
    func=l2f.lut2func(dum['lut'],dum['axes'])    
    def jfunc(woo):
        return func(woo).reshape(dum['ny'],dum['nx'])
    return jfunc
    

if __name__ == '__main__':
    #How to use
    # first create a LUT 
    luta=np.arange(240000,dtype=np.float).reshape(6,40000,order='C')
    lutb=np.arange(240000,dtype=np.float).reshape(6,40000,order='F')**2
    lutc=np.sqrt(np.arange(240000,dtype=np.float).reshape(6,40000,order='F'))
    # either as Tuple 
    luts1=(luta,lutb,lutc)
    # or as single np.array
    luts2=np.array((luta,lutb,lutc)).transpose([1,2,0])

    #second create the axes 
    xx1=np.array([3.,4.,6.,7.,9.,15.])
    xx2=np.linspace(-10.,30.,40000)
    #as a tuple
    axes=(xx1,xx2)
    
    #finaly create the func
    func1=l2f.lut2func(luts1,axes)
    func2=l2f.lut2func(luts2,axes)
    
    
    #for the jacobians
    #use the function luts
    jlut= generate_jacobian_lut(luts2,axes)
    #save the jacobians 
    lut2ncdf(jlut,'jlut_test.nc')
    #and make a function from it
    jfun=ncdf2func('jlut_test.nc')
    
    # now test the jacobian function:
    print jfun([3.,10.]) 
    #and compare it with a numerical_jacoby
    a=np.array([3,1])
    b=np.array([15,15])
    x=np.array([3,10.])
    print  numerical_jacoby(a, b, x, func1, 2, 3, delta=0.01)
    
    
    import time
    t=time.time()
    for i in range(1000): dum=jfun(x)
    print 'jfun takes %i us' %((time.time()-t)*1000)
    t=time.time()
    for i in range(1000): dum=numerical_jacoby(a, b, x, func2, 2, 3, delta=0.01)
    print 'numerical takes %i us' %((time.time()-t)*1000)
    
    


