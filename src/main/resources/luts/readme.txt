We need three LUTs from old Wadamo code in this folder:
wadamo_core_meris.json
wadamo_core_modis_aqua.json
wadamo_core_modis_terra.json

They are too large for GitHub repository, so get them from
fs1:\projects\ongoing\Wadamo\software\wadamo_0.9.012.tgz, and
DO NOT ADD THEM TO GIT VERSION CONTROL HERE!!

------------------------------------------------------------------

For new TCWV processor we need more LUTs:
land/land_core_meris.nc4
land/land_core_modis_aqua.nc4
land/land_core_modis_terra.nc4
ocean/ocean_core_meris.nc4
ocean/ocean_core_modis_aqua.nc4
ocean/ocean_core_modis_terra.nc4

Get them from
fs1/projects/ongoing/CAWA/software/from_rene/cawa_tcwv_1.00.080.tgz
DO NOT ADD THEM TO GIT VERSION CONTROL HERE!!

------------------------------------------------------------------

For new CTP processor we need more LUTs:
cloud_complete_core_meris.nc4
cloud_core_meris.nc4
ws_alb_10_2005.nc4
cloud_complete_core_olci.nc4
cloud_core_olci.nc4

Get them from
fs1/projects/ongoing/CAWA/software/from_rene/cawa_cloud_0.10.026.tgz
DO NOT ADD THEM TO GIT VERSION CONTROL HERE!!

In the TGZ there are also MERIS and OLCI source products for the demo:
- cawa_cloud_0.10.026/demo/MER_RR__1PRACR20070601_090923_000026432058_00351_27459_0000.h5
- cawa_cloud_0.10.026/demoS3A_OL_1_EFR____20160531T093141_20160531T093441_20160531T113517_0179_004_364_2160_MAR_O_NR_001.SEN3.tgz
- cawa_cloud_0.10.026/demoS3A_OL_1_EFR____20161110T104930_20161110T105230_20161110T124719_0179_010_379_2340_MAR_O_NR_002.SEN3.tgz