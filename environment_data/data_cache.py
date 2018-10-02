import os
import pickle

from environment_data import custom_logger

custom_logger = custom_logger.CustomLogger()
logger = custom_logger.get_logger(__name__)


class DataCache:

    def __get_pickle_file_path(self, file_path):
        base_name = os.path.basename(file_path)
        file_name = base_name.split('.')[0]
        full_name = ''.join([file_name, ".", "cache"])

        pickle_path = os.path.join('weather_data_cache', full_name)
        return pickle_path

    def load_cache(self, file_path, return_object):
        pickle_path = self.__get_pickle_file_path(file_path)

        if os.path.exists(pickle_path):
            pickle_file = open(pickle_path, "rb")
            temp_object = pickle.Unpickler(pickle_file).load()

            logger.info(
                "Cached Database was loaded. | Database Name: {} | Path: {}".format(file_path, pickle_path))
            pickle_file.close()

            return_object = temp_object
        else:
            logger.warning(
                "Cached Database was not found. | Database Name: {} | Path: {}".format(file_path,
                                                                                       pickle_path))

        return return_object

    def store_cache(self, file_path, object_data):
        pickle_path = self.__get_pickle_file_path(file_path)

        if not os.path.exists(pickle_path):
            pickle_file = open(pickle_path, "wb")
            pickle.Pickler(pickle_file, pickle.HIGHEST_PROTOCOL).dump(object_data)
            pickle_file.close()

            logger.info(
                "Cached Database was created successfully. | Database Name: {} | Path: {}".format(file_path,
                                                                                                  pickle_path))
