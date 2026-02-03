# coding: utf-8

from __future__ import annotations # Für zukünftige Typ-Hints
from typing import Any, Dict, Type

import os
import shelve

import pymongo

import config


class DataCache:
    """Ein Cache-System, das Shelve zur Persistenz verwendet."""

    main_db: str = 'store.cache'

    def __init__(self) -> None:
        script_dir: str = os.path.dirname(__file__)
        abs_file_path: str = os.path.join(script_dir, self.main_db)

        self.shelve_db = shelve.open(abs_file_path)

    def load_dict(self, attribute_name: str) -> Dict[str, Any]:
        """Lädt ein Dictionary aus dem Cache.

        Args:
            attribute_name: Der Name des Attributs, dessen Dictionary geladen werden soll.

        Returns:
            Das geladene Dictionary oder ein leeres Dictionary, falls nicht vorhanden.
        """
        return_dict: Dict[str, Any] = dict()

        if attribute_name in self.shelve_db:
            return_dict = self.shelve_db[attribute_name]

        return return_dict

    def store_dict(self, attribute_name: str, store_dict: Dict[str, Any]) -> None:
        """Speichert ein Dictionary im Cache.

        Args:
            attribute_name: Der Name des Attributs, dessen Dictionary gespeichert werden soll.
            store_dict: Das zu speichernde Dictionary.
        """
        self.shelve_db[attribute_name] = store_dict

    def __enter__(self) -> DataCache:
        return self

    def __exit__(self, exc_type: Type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: Any | None) -> None:
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
