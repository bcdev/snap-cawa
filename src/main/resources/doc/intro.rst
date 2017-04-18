.. _intro:

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

This document is the User Manual for the SNAP TCWV and CTP processors written in `Python <http://www.python.org>`_ and
`Java <http://www.oracle.com/java>`_ which have been developed in the frame of the CAWA
project. Its purpose is to describe in detail how to obtain, install and operate these processors. Also, a
comprehensive overview of all related data products (input as well as intermediate and final products) is provided.

The explicit structure of the document is as follows:

* Chapter 1 is this introduction.
* `Chapter 2 <cawa_processing_system.html>`_ gives an overview of the SNAP CAWA TCWV and CTP processing system.
* `Chapter 3 <cawa_products.html>`_ describes all relevant SNAP CAWA products.
* `Chapter 4 <cawa_installation.html>`_ explains how to get and install the processing software.
* `Chapter 5 <cawa_usage.html>`_ explains how to run the processing software.
* `Chapter 6 <cawa_scenarios.html>`_ gives an example for a typical CAWA processing use case.
* `Chapter 7 <cawa_monitoring.html>`_ shows possibilities how to monitor the processing.
* `Chapter 8 <cawa_troubleshooting.html>`_ describes troubleshooting options.
* `Chapter 9 <annex.html>`_ contains various annexes.

References
==========

.. todo:: OD to complete

1.  ADVANCED CLOUDS, AEROSOLS AND WATER VAPOUR PRODUCTS FOR SENTINEL-3/OLCI: Technical, Management and
    Financial Proposal. Issue 1.0, 28.03.2014.

2.  Retrieval for Total Coulumn Water Vapor from MERIS/OLCI and MODIS for Land- and Ocean Surfaces. CAWA TCWV ATBD,
    available at: https://earth.esa.int/web/sppa/activities/cawa/projects-documents

3.  Retrieval of Cloud Top Pressure from MERIS and  OLCI O2 A-Band Measurements. CAWA CTP ATBD,
    available at: https://earth.esa.int/web/sppa/activities/cawa/projects-documents

4.  The Sentinel Application Platform (SNAP),
    available at: http://step.esa.int/main/toolboxes/snap/

5.  Configure Python to use the SNAP-Python (snappy) interface,
    available at: https://senbox.atlassian.net/wiki/display/SNAP/Configure+Python+to+use+the+SNAP-Python+%28snappy%29+interface

6.  CoastColour Project Web Site,
    available at: http://www.coastcolour.org

7.  OceanColour Project Web Site,
    available at: http://www.esa-oceancolour-cci.org

8.  Bourg, L. (2009): MERIS Level 2 Detailed Processing Model. ACRI-ST, Document No. PO-TN-MEL-GS-0006, 15 July 2009.

9. GlobAlbedo Project Web Site,
    available at: http://globalbedo.org

10. LandCover Project Web Site,
    available at: http://www.esa-landcover-cci.org

11. GlobAlbedo ATBD 'Pixel Classification'. Version 4.1, 26 June 2012.

12. ERA-Interim global atmospheric reanalysis dataset,
    available at: http://www.ecmwf.int/en/research/climate-reanalysis/era-interim


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

Copyright (C) 2014-2017  ESA / Brockmann Consult.

.. index:: Data Policy

Data Policy
===========

.. todo:: OD to complete
