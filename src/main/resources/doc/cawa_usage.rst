.. _cawa_usage:

=======================================
How to run the CAWA Processing Software
=======================================


The Pixel Classification Step
=============================

The pixel classification with IdePix is applied on the L1b input products. The operators for MERIS and MODIS

- Idepix.Meris
- Idepix.Modis

are invoked via the SNAP gpt tool like:
::
    <operator-name> -SsourceProduct=<path-to-L1b-product> -f NetCDF4-BEAM -t <path-to-target-product>

Processing Parameters
---------------------

The gpt command given above invokes the usage of default processing parameters.
A list of possible processing parameters for the IdePix pixel classification can be obtained from:
::
    $SNAP_INSTALL_DIR/bin/gpt -h <operator-name>


TCWV Processing
===============

The TCWV processing is applied on the 'extended' IdePix products as described in :ref:`cawa_products`.
The operators for MERIS and MODIS

- cawa_tcwv_meris_op
- cawa_tcwv_modis_op

are invoked via the SNAP gpt tool like:
::
    <operator-name> -SsourceProduct=<path-to-IdePix-product> -f NetCDF4-CAWA -t <path-to-target-product>


Processing Parameters
---------------------

A list of possible processing parameters for the MERIS/MODIS TCWV processing can be obtained from:
::
    $SNAP_INSTALL_DIR/bin/gpt -h cawa_tcwv_meris_op
    $SNAP_INSTALL_DIR/bin/gpt -h cawa_tcwv_modis_op

CTP Processing
==============

The CTP processing is applied on the 'extended' IdePix products as described in :ref:`cawa_products`.
The operator

- cawa_ctp_meris_op

is invoked via the SNAP gpt tool like:
::
    <operator-name> -SsourceProduct=<path-to-IdePix-product> -f NetCDF4-CAWA -t <path-to-target-product>

Processing Parameters
---------------------

A list of possible processing parameters for the MERIS CTP processing can be obtained from:
::
    $SNAP_INSTALL_DIR/bin/gpt -h cawa_ctp_meris_op


Data Analysis Tools
===================

SNAP Desktop Application
------------------------

