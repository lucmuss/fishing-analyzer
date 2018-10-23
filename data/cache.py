# coding: utf-8

import os
import shelve


class DataCache:
    main_db = 'store.cache'

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, self.main_db)

        self.shelve_db = shelve.open(abs_file_path)

    def load_dict(self, attribute_name):
        return_dict = dict()

        if attribute_name in self.shelve_db:
            return_dict = self.shelve_db[attribute_name]

        return return_dict

    def store_dict(self, attribute_name, store_dict):
        self.shelve_db[attribute_name] = store_dict

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shelve_db.close()
