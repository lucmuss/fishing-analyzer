import os
import pickle
import shelve


class DataCache:
    main_db = 'store.cache'

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, self.main_db)

        self.shelve_db = shelve.open(abs_file_path)

    def load_dict(self, attribute_name):
        return_object = dict()

        if attribute_name in self.shelve_db:
            return_object = self.shelve_db[attribute_name]

        return return_object

    def store_dict(self, attribute_name, object_dict):
        self.shelve_db[attribute_name] = object_dict

    def __exit__(self):
        self.shelve_db.close()
