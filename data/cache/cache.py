import os
import pickle


class DataCache:

    def __get_cache_file_path(self, attribute_name):
        cache_name = ''.join([attribute_name, ".", "cache"])

        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, cache_name)

        return abs_file_path

    def load_cache(self, attribute_name, return_object):
        cache_path = self.__get_cache_file_path(attribute_name)

        if os.path.exists(cache_path):
            pickle_file = open(cache_path, "rb")
            temp_object = pickle.Unpickler(pickle_file).load()

            pickle_file.close()

            return_object = temp_object

        return return_object

    def store_cache(self, file_path, object_data):
        cache_path = self.__get_cache_file_path(file_path)

        if not os.path.exists(cache_path):
            pickle_file = open(cache_path, "wb")
            pickle.Pickler(pickle_file, pickle.HIGHEST_PROTOCOL).dump(object_data)
            pickle_file.close()
