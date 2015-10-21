from __future__ import print_function
import sys
import os
import subprocess


CSI="\x1B["
INST=('meris','modis_terra','modis_aqua')
TSTDIR=os.path.realpath(os.path.dirname(__file__))



def redprint(st):
    print(CSI+"31;40m" + st + CSI + "0m") 
def greenprint(st):
    print(CSI+"32;40m" + st + CSI + "0m") 

def okprint(ok):
    if ok is True: greenprint('    passed\n')
    else:redprint('    failed\n')
        


def test_modules():
    ok=True
    print('   Testing existence of needed standard modules: ', end="")
    needed_modules=('numpy','scipy','netCDF4','shutil','time','numpy.f2py','re')
    ok=True
    for nm in needed_modules:
        print(' %s,'%nm, end="")
    print('')    
    for nm in needed_modules:
        try:
            dum=__import__(nm) 
        except :
            redprint('     Module %s could not imported. You may have a problem'%nm)
            ok=False
    return ok        

def test_python_version():
    ok=True
    print('   Testing python version: %i.%i.%i'% (sys.version_info[0:3]))
    if sys.version_info < (2, 7, 1):
            redprint('     To old, you need at least python 2.7.1')
            ok=False
    if sys.version_info >= (3, 0, 0):
            redprint('     Python 3.x is not yet supported (but should be easy,,)' )
            ok=False
    return ok

def test_ipython_version():
    ok=True
    print('   Testing if ipython is installed')
    try:
        import IPython
    except Exception, e:
        print('')
        print('     '+str(e))
        redprint('     Ipython could not imported. You may have a problem runing the demo.')
        ok=False
    if ok is True:
        ver=IPython.release.version
        ver =tuple([int(i) for i in ver.split('.')])
        print('   Testing ipython version: %i.%i.%i'% (ver))
        if ver < (0,13,2):
                redprint('     Perhabs to old, I used ipython 0.13.2')
                ok=False
    return ok


def test_numpy_version():
    ok=True
    import numpy as np
    ver=np.version.version
    ver =tuple([int(i) for i in ver.split('.')])
    print('   Testing numpy version: %i.%i.%i'%ver )
    if ver < (1, 9, 0):
            ok=False
            redprint('     Older than my version. May work neverthelss.')
    return ok


# def test_fortran_version():
#     ok=True
#     print('   Testing fortran: ', end="")
#     aa=os.system('which gfortran &> /dev/null')
#     if aa != 0:
#         ok= False
#         print('')
#         redprint('     Error searching gfortran.')
#     else:
#         import re
#         ver=re.findall('\d+\.\d+\.\d+',
#                     os.popen("gfortran --version").readline())[0]
#         print(ver)
#         ver =tuple([int(i) for i in ver.split('.')])
#         if ver < (4,8,3):
#             redprint('     Not tested with older version than 4.8.3.')
#             redprint('     Nevertheless, %i.%i.%i should work.'%ver)
#     return ok
#
# def test_f2py():
#     ok=True
#     print('   Testing numpy f2py:')
#     #removing old , if exists
#     dots=('dot.so','dot.f','dot.f.log')
#     for ff in dots:
#         if os.path.isfile(ff):
#             os.remove(ff)
#     source=[
#     '      subroutine dot(x,y,z,dx1,dxy,dy2)\n',
#     'cf2py intent(in) :: x,y\n',
#     'cf2py intent(out) :: z\n',
#     'cf2py intent(hide) :: dx1,dxy,dy2\n',
#     'cf2py double :: x(dx1,dxy),y(dxy,dy2),z(dx1,dy2)\n',
#     '      implicit none\n',
#     '      integer dx1,dxy,dy2\n',
#     '      integer ix1,ixy,iy2\n',
#     '      double precision x(dx1,dxy),y(dxy,dy2),z(dx1,dy2)\n',
#     '      do 100 ix1=1,dx1\n',
#     '      do 200 iy2=1,dy2\n',
#     '        z(ix1,iy2)=0.d0\n',
#     '        do 300 ixy=1,dxy\n',
#     '            z(ix1,iy2)=z(ix1,iy2)+ x(ix1,ixy)*y(ixy,iy2)\n',
#     '300     enddo \n',
#     '200   enddo\n',
#     '100   enddo\n',
#     '      end\n']
#
#     with open('dot.f','w') as f:
#         f.writelines(source)
#     aa=os.system('f2py -m dot -c dot.f &>dot.f.log')
#     if aa != 0:
#         ok= False
#         redprint('     Error compiling test function. Check dot.f.log')
#     else:
#         if not os.path.isfile('dot.so'):
#             redprint('     Module dot.so does not exist. Is the gfortran compiler installed?')
#             ok=False
#         try:
#             sys.path.append(os.getcwd())
#             import numpy
#             import dot
#             a=numpy.arange(12.).reshape(1,12)
#             b=numpy.arange(12.).reshape(12,1)
#             if a.dot(b)[0,0] != dot.dot(a,b)[0,0]:
#                 redprint('     Module dot does not work as expected. Hm... ask Rene?')
#                 ok=False
#         except Exception, e:
#             print('')
#             print('     '+e)
#             redprint('     Module dot could not imported. Is the gfortran compiler installed?')
#             ok=False
#     if ok is True:
#         for ff in dots:
#             if os.path.isfile(ff):
#                 os.remove(ff)
#     return ok

def test_luts():
    ok=True
    from netCDF4 import Dataset
    print('   Testing look up tables:')
    for inst in INST:
        for ls in ('land','ocean'):
            print('       %s_core_%s.nc4'%(ls,inst))
    for inst in INST:
        for ls in ('land','ocean'):
            ff='%s/../luts/%s/%s_core_%s.nc4'%(TSTDIR,ls,ls,inst)
            if not os.path.isfile(ff):
                redprint('     Can not find: %s'%ff)
                ok=False
            else:
                with Dataset(ff,'r') as nc:
                    try: 
                        if 'lut' not in nc.variables:
                            ok=False
                            redprint('      Can not find "lut" in  %s'%ff)
                    except:
                        ok=False
                        redprint('       Can not read  %s. Corrupt?'%ff)
    return ok



if __name__=='__main__':
    
    for test in (test_python_version,test_modules,test_numpy_version,
                 test_luts,test_ipython_version):
        okprint(test())
           










   
