import json
import os
from typing import Any, Dict

from codeintp.bot_utils.datautil.interface import FileDataUtilInterface
from codeintp.bot_utils.logger import bot_logger


class JSONDataUtil(FileDataUtilInterface):
    def _open_table(self, table_name: str):
        file_path = f'data/{table_name}.json'
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def initialize(table_name: str):
        try:
            os.makedirs("data", exist_ok=True)
            if not os.path.exists(f"data/{table_name}.json"):
                with open(f"data/{table_name}.json", 'w') as f:
                    json.dump({}, f, indent=4)
        except Exception as e:
            bot_logger.error(f"Error initializing a table: {e}")

    def add(self, table_name: str, data_object: Dict[str, Any]):
        key_prefix = "_key."
        key_candidates = [key for key in data_object if key.startswith(key_prefix)]
        if len(key_candidates) != 1:
            raise ValueError("Data object must contain exactly one key with '_key.' prefix")
        new_key = key_candidates[0][len(key_prefix):]
        data_object.pop(key_candidates[0])
        try:
            jobj = self._open_table(table_name)
            jobj[new_key] = data_object
            with open(f"data/{table_name}.json", "w") as file:
                json.dump(jobj, file, indent=4)
        except Exception as e:
            bot_logger.error(f"Error adding data to {table_name}: {e}")

    def delete(self, table_name: str, identifier: str):
        _, identifier_value = identifier.split("_", 1)
        try:
            jobj = self._open_table(table_name)
            jobj.pop(identifier_value, None)
            with open(f"data/{table_name}.json", "w") as file:
                json.dump(jobj, file, indent=4)
        except Exception as e:
            bot_logger.error(f"Error deleting data from {table_name}: {e}")

    def _loop_search(self, table, identifier: str = ""):
        identifier_key, identifier_value = identifier.split("_", 1)
        return [item for item in table.values() if item.get(identifier_key) == identifier_value] or None

    def lookup(self, table_name: str, identifier: str = "", search: bool = False, is_here: bool = False):
        if identifier:
            _, identifier_value = identifier.split("_", 1)
        else:
            identifier_value = identifier
        try:
            jobj = self._open_table(table_name)
            if not identifier:
                return jobj
            elif search:
                return self._loop_search(jobj, identifier)
            return jobj.get(identifier_value)
        except Exception as e:
            if not is_here:
                bot_logger.error(f"Error looking up data from {table_name}: {e}")
            raise

    def modify(self, table_name: str, identifier: str, items: Dict[str, Any]):
        _, identifier_value = identifier.split("_", 1)
        try:
            jobj = self._open_table(table_name)
            obj = jobj[identifier_value]
            for item in items:
                if not isinstance(item, list) or len(item) != 2:
                    raise ValueError("Each item in the modified data must be a list of two elements [key, value].")
                key, value = item
                obj[key] = value
            with open(f"data/{table_name}.json", "w") as f:
                json.dump(jobj, f, indent=4)
        except Exception as e:
            bot_logger.error(f"Error modifying data from {table_name}: {e}")
