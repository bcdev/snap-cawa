import os

######################################################################################
# CAWA utils.
######################################################################################

# Idepix flags:
F_INVALID      = 1
F_CLOUD        = 2
F_CLOUD_BUFFER = 16
F_CLOUD_SHADOW = 32

class cawa_utils:



    def do_nothing(self):
        pass

    def calculate_pixel_mask(self, index, classif_data):
        return self.calculate_pixel_mask(classif_data[index])

    def calculate_pixel_mask(self, classif_data):
        """
        Exclude pixels classified as invalid, cloud, cloudbuffer, cloudshadow:
        # F_INVALID (1)
        """
        # print('classif_data[index]: ', classif_data[index])
        # print('classif_data[index] & F_INVALID: ', classif_data[index] & F_INVALID)
        # print('classif_data[index] & F_CLOUD: ', classif_data[index] & F_CLOUD)
        # print('classif_data[index] & F_CLOUD_BUFFER: ', classif_data[index] & F_CLOUD_BUFFER)
        # print('classif_data[index] & F_CLOUD_SHADOW: ', classif_data[index] & F_CLOUD_SHADOW)

        return_value =  classif_data & F_INVALID == F_INVALID or \
                        classif_data & F_CLOUD == F_CLOUD
                        # classif_data & F_CLOUD == F_CLOUD or \
                        # classif_data & F_CLOUD_BUFFER == F_CLOUD_BUFFER or \ todo: discuss buffer/shadow
                        # classif_data & F_CLOUD_SHADOW == F_CLOUD_SHADOW

        return return_value


