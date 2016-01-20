######################################################################################
# CAWA utils.
######################################################################################

# Idepix flags (MERIS):
L1_INVALID = 128
F_INVALID = 1
F_CLOUD = 2
F_CLOUD_BUFFER = 4
F_CLOUD_SHADOW = 8
F_LAND = 128


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

        return_value = l1_flag & L1_INVALID == L1_INVALID or \
                       classif_flag & F_INVALID == F_INVALID or \
                       classif_flag & F_CLOUD == F_CLOUD or \
                       classif_flag & F_CLOUD_BUFFER == F_CLOUD_BUFFER or \
                       classif_flag & F_CLOUD_SHADOW == F_CLOUD_SHADOW
        # todo: discuss if we want cloud buffer (yes - RP 20160119) and/or cloud shadow

        return return_value

    @staticmethod
    def is_meris_land_pixel(classif_flag):
        """
        Determines from Idepix flag if pixel is land pixel
        :param classif_flag:
        :return: 1 if MERIS pixel is land, 0 otherwise
        """

        return classif_flag & F_LAND == F_LAND
        # todo: provide for MODIS accordingly

    @staticmethod
    def band_exists(name, band_names):
        for band_name in band_names:
            if name == band_name:
                return True
        return False
