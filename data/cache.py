# coding: utf-8

import os
import shelve
import pymongo
import config


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


class DatabaseDataCache:

    def __init__(self, database_model):
        self.database_model = database_model

    def load_dict(self, attribute_name):
        return_dict = dict()

        collection_names = self.database_model.mongo_db.collection_names()

        if attribute_name in collection_names:
            mongo_collection = self.database_model.mongo_db.get_collection(attribute_name)

            return_dict = mongo_collection.find_one()
            return_dict.pop('_id', None)

        return return_dict

    def store_dict(self, attribute_name, store_dict):
        collection_names = self.database_model.mongo_db.collection_names()

        if not attribute_name in collection_names:
            self.database_model.mongo_db.create_collection(attribute_name)

            mongo_collection = self.database_model.mongo_db.get_collection(attribute_name)

            mongo_collection.insert_one(store_dict)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database_model.mongo_db.close()


if __name__ == '__main__':
    with DataCache as dc:
        air = dc.load_dict('air_temperature')

    with DatabaseDataCache as dc:
        air = dc.load_dict('air_temperature')
