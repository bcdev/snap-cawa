==================================
A typical CAWA Processing Use Case
==================================

.. BC

Depending on the specific question, the user can extract different types of data subsets from the Earth System Data Cube (ESDC)
for further processing and analysis with specialized methods from the
`Data Analytics Toolkit <dat_usage.html#the-data-analytics-toolkit>`__. For example,

* investigating the data cube **at a single geographic location**, the user obtains multivariate time series for each
  longitude-latitude pair. These time series can be investigated using established methods of multivariate time series
  analysis, and afterwards the results can be merged onto a global grid again.
* Assessing the data-cube **at single time stamps** results in synoptic geospatial maps,
  whose properties can be investigated with geostatistical methods.
* It is also possible to perform **univariate spatiotemporal analyses** on single variables extracted from the
  Data Cube. 
* The main objective is, however, to develop **multivariate spatiotemporal analyses** by utilizing the entire 4D ESDC.
  Following this avenue unravels the full potential of the ESDC and may provide a holistic view on the entire Earth System.

The ESDC allows for all these approaches, because all variables are available on a common spatiotemporal grid, which greatly
reduces the pre-processing efforts typically required to establish consistency among data from different sources.




