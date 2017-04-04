.. index:: SNAP Cawa TCWV and CTP Processing System

============================================
The SNAP Cawa TCWV and CTP Processing System
============================================

Overview
========

The key goal of the CAWA project regarding software development, production and dissemination was to
implement the proposed algorithms for TCWV and CTP in free and easily accessible open source toolboxes, notably and
foremost ESA’s SNAP toolbox. After successful implementation, TCWV and CTP datasets from the full MERIS archive were
generated with BC's 'Calvalus' Linux cluster following the project targets. In addition, TCWV from several months
of 'OLCI-like' input datasets (i.e. MODIS Aqua/Terra products MOD021 and MYD021) were generated. However, the SNAP
TCWV and CTP processors are in principle fully portable and can be run on any Linux platform. The procedure for
installation and operation is described in this chapter.

.. index:: Theoretical Background Summary

Theoretical Background
======================

The motivation and theoretical background for the TCWV and CTP retrieval is summarized in the CAWA project
proposal [`1 <intro.html#References>`_].
The underlying algorithms are described in detail in the corresponding ATBDs for TCWV [`2 <intro.html#References>`_]
and CTP [`3 <intro.html#References>`_], respectively.

.. index:: Processing Flow

Processing Flow
===============

Although the TCWV and CTP processors are completely independent of each other, their individual processing flow is very
similar as shown and explained below.

The SNAP Graph Processing Framework
-----------------------------------

A common architecture for all Sentinel Toolboxes is being jointly developed by Brockmann Consult, Array Systems
Computing and C-S called the Sentinel Application Platform (SNAP).

The SNAP architecture is ideal for Earth Observation processing and analysis due to various technological
innovations as well as approved concepts from the BEAM toolbox. One of the key components in SNAP is the Graph
Processing Framework (GPF) for creating user-defined processing chains. Both CAWA TCWV and CTP processors make use of this
framework.

A good starting point for more detailed information is the SNAP homepage [`4 <intro.html#References>`_] and also the help
documentation integrated in the SNAP desktop application.

The SNAP-Python Interface (SNAPPY)
----------------------------------

A new concept provided in SNAP is the possibility to develop preocessing scripts using Python. This is realized by a new
SNAP-Python interface (SNAPPY). This component can also be used from the Graph Processing Framework so that in SNAP scientific
GPF processors can be developed not only in Java, but now also in Python. In CAWA, both TCWV and CTP processors
are making use of this and were written in Python, whereas the pre-processing (i.e. the IdePix pixel classification) uses a
GPF processor which was written in Java.

More detailed information on SNAPPY can be found in [`5 <intro.html#References>`_].


TCWV Processor
--------------

The overall processing flow of the SNAP TCWV processor is shown in :numref:`tcwv_chain`.

.. _tcwv_chain:
.. figure::  pix/tcwv_chain.png
   :align:   center
   :scale: 80 %

   Processing flow of the SNAP TCWV processor.



CTP Processor
-------------

The overall processing flow of the SNAP CTP processor is shown in :numref:`ctp_chain`.

.. _ctp_chain:
.. figure::  pix/ctp_chain.png
    :align:   center
    :scale: 80 %

    Processing flow of the SNAP CTP processor.

The data is organised in the described 4-dimensional form x(u,v,t,k), but additionally each data stream k is assigned to one
of the subsystems of interest:

* Land surface
* Atmospheric forcing
* Socio-economic data



.. index:: Processing Environment

Processing Environment
======================

The data is organised in the described 4-dimensional form x(u,v,t,k), but additionally each data stream k is assigned to one
of the subsystems of interest:

* Land surface
* Atmospheric forcing
* Socio-economic data

.. index:: Processor Components

Processor Components
====================

The data is organised in the described 4-dimensional form x(u,v,t,k), but additionally each data stream k is assigned to one
of the subsystems of interest:

* Land surface
* Atmospheric forcing
* Socio-economic data





