from __future__ import annotations

import os
import shelve
from typing import Any


class DataCache:
    """Persistent key-value cache backed by shelve."""

    main_db = "store.cache"

    def __init__(self) -> None:
        script_dir = os.path.dirname(__file__)
        self._cache_path = os.path.join(script_dir, self.main_db)

    def load_dict(self, attribute_name: str) -> dict[str, Any]:
        with shelve.open(self._cache_path) as shelf:
            return dict(shelf.get(attribute_name, {}))

    def store_dict(self, attribute_name: str, store_dict: dict[str, Any]) -> None:
        with shelve.open(self._cache_path, writeback=True) as shelf:
            shelf[attribute_name] = store_dict

    def __enter__(self) -> DataCache:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        return None


class DatabaseDataCache:
    """MongoDB-backed dictionary cache used by the environment data loaders."""

    def __init__(self, database_model: Any) -> None:
        self.database_model = database_model

    def load_dict(self, attribute_name: str) -> dict[str, Any]:
        collection_names = self.database_model.mongo_db.collection_names()
        if attribute_name not in collection_names:
            return {}

        mongo_collection = self.database_model.mongo_db.get_collection(attribute_name)
        return_dict = mongo_collection.find_one() or {}
        return_dict.pop("_id", None)
        return return_dict

    def store_dict(self, attribute_name: str, store_dict: dict[str, Any]) -> None:
        collection_names = self.database_model.mongo_db.collection_names()
        if attribute_name in collection_names:
            return

        self.database_model.mongo_db.create_collection(attribute_name)
        mongo_collection = self.database_model.mongo_db.get_collection(attribute_name)
        mongo_collection.insert_one(store_dict)

    def __enter__(self) -> DatabaseDataCache:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.database_model.mongo_db.close()
