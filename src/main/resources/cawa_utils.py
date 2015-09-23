import os

######################################################################################
# CAWA utils.
######################################################################################

# Idepix flags:
L1_INVALID      = 128
F_INVALID      = 1
F_CLOUD        = 2
F_CLOUD_BUFFER = 4
F_CLOUD_SHADOW = 8

class cawa_utils:



    def do_nothing(self):
        pass

    def calculate_pixel_mask_array(self, index, classif_data, l1_flag_data):
        return self.calculate_pixel_mask(classif_data[index], l1_flag_data[index])

    def calculate_pixel_mask(self, classif_data, l1_flag_data):
        """
        Exclude pixels classified as invalid, cloud, cloudbuffer, cloudshadow:
        # F_INVALID (1)
        """
        # print('classif_data[index]: ', classif_data[index])
        # print('classif_data[index] & F_INVALID: ', classif_data[index] & F_INVALID)
        # print('classif_data[index] & F_CLOUD: ', classif_data[index] & F_CLOUD)
        # print('classif_data[index] & F_CLOUD_BUFFER: ', classif_data[index] & F_CLOUD_BUFFER)
        # print('classif_data[index] & F_CLOUD_SHADOW: ', classif_data[index] & F_CLOUD_SHADOW)

        return_value =  l1_flag_data & L1_INVALID == L1_INVALID or \
                        classif_data & F_INVALID == F_INVALID or \
                        classif_data & F_CLOUD == F_CLOUD or \
                        classif_data & F_CLOUD_SHADOW == F_CLOUD_SHADOW
        # todo: discuss if we want cloud buffer and/or cloud shadow

        return return_value


