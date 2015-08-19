beam-wadamo
===========

This is the SNAP Cawa processor, based on GPF and the bi-directional Python-Java bridge (JPY)

Some short instructions:
### TODO: adapt description to SNAP/Cawa enviromnemt!! ###

- to get the wadamo_op running as a BEAM GPF operator, all steps
** get python libraries from the fortran sources
** install jpy
** install beampy
** put everything at the right place
has to be done in advance, precisely following the according separate documentations.
UP TO NOW, ALL THIS WAS WORKING ONLY IN A PURE 32BIT ENVIRONMENT, HAVING ONLY ONE PYTHON INSTALLED (PYTHON 2.7.8 32BIT)!
MAKE SURE YOU DO NOT MIX UP ANYTHING WITH 64BIT BY ACCIDENT!

--> The *.py files (including the wadamo_core.py) are expected in $BEAM_HOME/modules/beam-wadamo
--> The wadamo_op-info.xml is expected in $BEAM_HOME/modules/beam-wadamo
--> The json luts (MERIS, MODIS A/T) are expected in $BEAM_HOME/modules/beam-wadamo/luts
--> The 'beampy-operators' file is expected in $BEAM_HOME/modules/beam-wadamo/META-INF/services
--> The f2py libraries (wadamo_interpolators.pyd, wadamo_poly.pyd) are expected in the ../Lib/site-package
  folder of the Python installation dir.

If everything is fine, the operator can be called with a 32bit BEAM gpt like:
- gpt py_wadamo_op -Ssource=<L1b source>


