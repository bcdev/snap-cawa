.. index:: SNAP Cawa TCWV and CTP Processing System

============================================
The SNAP Cawa TCWV and CTP Processing System
============================================

.. BC

Overview
========

Earth observations (EOs) are usually produced and treated as 3- dimensional singular data cubes, i.e. for each
longitude u ∈ {1, ..., Lon}, each latitude v ∈ {1, …, Lat}, and each time step t ∈ {1,...,T} an observation
X = {x(u,v,t)} ∈ R is defined. The challenge is, however, to take advantage of the numerous
EO streams and to explore them simultaneously.
Hence, the idea is to concatenate data streams such that we obtain a 4-dimensional data cube of the form x(u,v,t,k)
where k ∈ {1, …, N} denotes the index of the data stream. The focus of this project is therefore on learning how
to efficiently and reliably create, curate, and explore a 4-dimensional Earth System Data Cube (ESDC).
If feasible, the included data-sets contain uncertainty information. Limitations associated with the transformation
from source format into the ESDC format are explained in the `description of the data sets <annex.html#Annexes>`__.
The ESDC does not exhibit spatial or temporal gaps, since gaps in the source data are filled during ingestion into
the ESDC. While all observational values are conserved, gaps are filled with synthetic data, i.e. with data that is created by an
adequate gap-filling algorithm. Proper data flags ensure an unambiguous distinction between observational and
synthetic data values.


.. index:: Theoretical Background Summary

Theoretical Background Summary
==============================

The data is organised in the described 4-dimensional form x(u,v,t,k), but additionally each data stream k is assigned to one
of the subsystems of interest:

* Land surface
* Atmospheric forcing
* Socio-economic data


.. index:: Processing Flow

Processing Flow
===============

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





