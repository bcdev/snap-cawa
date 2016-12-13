######################################################################################
# CAWA utils.
######################################################################################

# Idepix flags (MERIS):
# CAWA_MERIS_L1_INVALID = 128
# CAWA_MERIS_IDEPIX_INVALID = 1        # 2^0 for F_INVALID = 0 in Idepix v2.2.21 (20160128)
# CAWA_MERIS_IDEPIX_CLOUD = 2          # 2^1 for F_CLOUD = 1 in Idepix v2.2.21 (20160128)
# CAWA_MERIS_IDEPIX_CLOUD_BUFFER = 4   # 2^2 for F_CLOUD_BUFFER = 2 in Idepix v2.2.21 (20160128)
# CAWA_MERIS_IDEPIX_CLOUD_SHADOW = 8   # 2^3 for F_CLOUD_SHADOW = 3 in Idepix v2.2.21 (20160128)
# CAWA_MERIS_IDEPIX_LAND = 128         # 2^7 for F_LAND = 7 in Idepix v2.2.21 (20160128)


# NOTE: in Idepix v2.2.36 (20160802) used on Calvalus we have:
# public static final int F_INVALID = 0;
# public static final int F_CLOUD = 1;
# public static final int F_CLOUD_AMBIGUOUS = 2;
# public static final int F_CLOUD_SURE = 3;
# public static final int F_CLOUD_BUFFER = 4;
# public static final int F_CLOUD_SHADOW = 5;
# public static final int F_SNOW_ICE = 6;
# public static final int F_GLINTRISK = 7;
# public static final int F_COASTLINE = 8;
# public static final int F_LAND = 9;

CAWA_MERIS_IDEPIX_INVALID = 1        # 2^0 for F_INVALID = 0 in latest Idepixes > v2.2.36
CAWA_MERIS_IDEPIX_CLOUD = 2          # 2^1 for F_CLOUD = 1 in
CAWA_MERIS_IDEPIX_CLOUD_BUFFER = 16   # 2^4 for F_CLOUD_BUFFER = 4
CAWA_MERIS_IDEPIX_CLOUD_SHADOW = 32   # 2^5 for F_CLOUD_SHADOW = 5
CAWA_MERIS_IDEPIX_LAND = 512         # 2^9 for F_LAND = 9

# MODIS in latest Idepixes > v2.2.36:
# public static final int F_INVALID = 0;
# public static final int F_CLOUD = 1;
# public static final int F_CLOUD_AMBIGUOUS = 2;
# public static final int F_CLOUD_SURE = 3;
# public static final int F_CLOUD_BUFFER = 4;
# public static final int F_CLOUD_SHADOW = 5;
# public static final int F_CLOUD_B_NIR = 6;
# public static final int F_SNOW_ICE = 7;
# public static final int F_WHITE_ICE = 8;
# public static final int F_WET_ICE = 9;
# public static final int F_MIXED_PIXEL = 10;
# public static final int F_GLINT_RISK = 11;
# public static final int F_COASTLINE = 12;
# public static final int F_LAND = 13;
# public static final int F_BRIGHT = 14;

CAWA_MODIS_IDEPIX_INVALID = 1         # 2^0 for F_INVALID = 0 in latest Idepixes > v2.2.36
CAWA_MODIS_IDEPIX_CLOUD_SURE = 8      # 2^3 for F_CLOUD_SURE = 3
CAWA_MODIS_IDEPIX_CLOUD_BUFFER = 16   # 2^4 for F_CLOUD_BUFFER = 4
#CAWA_MODIS_IDEPIX_LAND = 8192         # 2^13 for F_LAND = 13
CAWA_MODIS_IDEPIX_LAND = 1024         # SNAP Idepix!

# noinspection PyUnresolvedReferences
class CawaUtils:
    """
    CAWA utility class
    Author: O.Danne
    """

    def __init__(self):
        pass

    @staticmethod
    def calculate_meris_pixel_mask(classif_flag, l1_flag):
        """
        Pixel mask: Exclude pixels classified as invalid, cloud, cloudbuffer, cloudshadow
        :param classif_flag
        :param l1_flag
        :return: 1 if pixel is invalid, 0 otherwise
        """

        # return_value = l1_flag & CAWA_MERIS_L1_INVALID == CAWA_MERIS_L1_INVALID or \
        return_value = classif_flag & CAWA_MERIS_IDEPIX_INVALID == CAWA_MERIS_IDEPIX_INVALID or \
                       classif_flag & CAWA_MERIS_IDEPIX_CLOUD == CAWA_MERIS_IDEPIX_CLOUD or \
                       classif_flag & CAWA_MERIS_IDEPIX_CLOUD_BUFFER == CAWA_MERIS_IDEPIX_CLOUD_BUFFER or \
                       classif_flag & CAWA_MERIS_IDEPIX_CLOUD_SHADOW == CAWA_MERIS_IDEPIX_CLOUD_SHADOW

        return return_value

    @staticmethod
    def calculate_modis_pixel_mask(classif_flag):
        """
        Pixel mask: Exclude pixels classified as invalid, cloud, cloudbuffer, cloudshadow
        We have no L1 flag from MODIS.
        :param classif_flag
        :return: 1 if pixel is invalid, 0 otherwise
        """

        return_value = classif_flag & CAWA_MODIS_IDEPIX_INVALID == CAWA_MODIS_IDEPIX_INVALID or \
                       classif_flag & CAWA_MODIS_IDEPIX_CLOUD_SURE == CAWA_MODIS_IDEPIX_CLOUD_SURE or \
                       classif_flag & CAWA_MODIS_IDEPIX_CLOUD_BUFFER == CAWA_MODIS_IDEPIX_CLOUD_BUFFER

        return return_value

    @staticmethod
    def is_land_pixel_meris(classif_flag):
        """
        Determines from Idepix flag if pixel is land pixel
        :param classif_flag:
        :return: 1 if MERIS pixel is land, 0 otherwise
        """

        return classif_flag & CAWA_MERIS_IDEPIX_LAND == CAWA_MERIS_IDEPIX_LAND

    @staticmethod
    def is_land_pixel_modis(classif_flag):
        """
        Determines from Idepix flag if pixel is land pixel
        :param classif_flag:
        :return: 1 if MERIS pixel is land, 0 otherwise
        """

        return classif_flag & CAWA_MODIS_IDEPIX_LAND == CAWA_MODIS_IDEPIX_LAND


    @staticmethod
    def band_exists(name, band_names):
        for band_name in band_names:
            if name == band_name:
                return True
        return False
