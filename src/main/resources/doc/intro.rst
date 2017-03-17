============
Introduction
============

Project background
==================

The SEOM S3 ‘advanced Clouds, Aerosols and WAter vapour products for Sentinel-3/OLCI’ CAWA project aims to the
development and improvement of advanced atmospheric retrieval algorithms for the Envisat/MERIS and Sentinel-3/OLCI
mission. A sensor comprehensive and consistent 1D-Var water vapour algorithm has been developed and applied to the MERIS,
MODIS and first available OLCI measurements. An innovative and consistent cloud top pressure 1D-Var procedure was defined
for MERIS and all three OLCI O2 A-band channels, which will significantly improve the retrieval accuracy. The
challenging and innovative GRASP algorithm for the retrieval of aerosols and surface properties has already shown
its advantage in comparison to conventional aerosol retrieval methods. All three algorithms will be further improved,
applied to the complete MERIS dataset, to a four months MODIS global time series and six months of OLCI data. We expect
to create improved consistent datasets of water vapour, cloud properties, namely cloud top pressure, and aerosol and
surface pressure. The intention of the CAWA team is to establish new and improved procedures to estimate atmospheric
properties, which also improve the retrieval of land and ocean properties.

.. bla

Purpose and Scope
=================

This Product Handbook is a living document that is under active development just as the CAB-LAB project itself.
Its purpose is to facilitate the usage of the BAVL and primarily targets scientists from various disciplines with a good
command of one of the supported high-level programming languages (`Python <http://www.python.org>`_, `Julia <http://julialang.org/>`_,
and `R <http://www.>`_), a solid background in the analysis of
large data-sets, and a sound understanding of the Earth System.
The focus of this document is therefore clearly on the description of the data and on the methods to access and manipulate the data.

In the final version, it is meant to be a self-contained documentation that enables the user to independently reap the full potential of the Earth System Data Cube (ESDC).
Developers may find a visit of the `project's git-hub pages <https://github.com/CAB-LAB>`_ worthwile.

The Product Handbook gives a general overview of the `ESCD's structure <cube_explanation.html#What is the Earth System Data Cube?>`__
and provide some examples to illustrate `potential uses of the system <cube_scenarios.html#What can I do with the Earth System Data Cube?>`__ .
The main part is considered with a detailed `technical description of the ESDC <cube_usage.html#How can I use the Earth System Data Cube?>`__
, which is accompanied by the full `specification of the API <api_reference.html#CAB-LAB API Reference>`__.
Finally, all data-sets included in the ESDC are listed and described in the `annex of the Product Handbook <annex.html#Annexes>`__.

References
==========

.. todo:: GB add more references here

1.  CAB-LAB's webpage: http://www.earthsystemdatacube.net

2.  CAB-LAB's github repository: https://github.com/CAB-LAB

Acronyms and Abbreviations
==========================

.. todo:: OD to complete

=======================  =============================================================================================
Acronym                     Definition
=======================  =============================================================================================
CAWA                     advanced Clouds, Aerosols and WAter vapour products
-----------------------  ---------------------------------------------------------------------------------------------
CTP                      Cloud Top Pressure
-----------------------  ---------------------------------------------------------------------------------------------
TCWV                     Total Column of Water Vapour
=======================  =============================================================================================

.. index:: Legal information

Legal information
=================

The CAWA TCWV and CTP processing software is free software:
you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.

Copyright (C) 2014-2017  The CAWA developer team.

.. index:: Data Policy

Data Policy
===========

The CAB-LAB team processes and distributes the data in the ESDC in good faith, but makes no warranty, expressed or implied,
nor assumes any legal liability or responsibility for any purpose for which the data are used.
In particular, the CAB-LAB team does not claim ownership of the data distributed through the ESDC nor does it alter the data
policy of the data owner. Therefore, the user is referred to the data owner for specific questions of data use.
References and more details of the data sets are listed in the `annex of the Product Handbook <annex.html#Annexes>`_.

The CAB-LAB team is thankful to have received permissions for re-distribution of all data contained in the ESDC from
the respective data owners.

.. note::

    Please cite the Earth System Data Cube as:

    The CAB-LAB developer team (2016). The Earth System Data Cube (Version 0.1), available at: https://github.com/CAB-LAB.
