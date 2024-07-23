from abc import abstractmethod, ABC
from typing import Any, Dict, Tuple, List, Union

from codeintp.bot_utils.logger import bot_logger


class DataUtilInterface(ABC):
    @abstractmethod
    def add(self, table_name: str, data_object: Dict[str, Any]):
        pass

    @abstractmethod
    def delete(self, table_name: str, identifier: str):
        pass

    @abstractmethod
    def lookup(self, table_name: str, identifier: str = "", is_here: bool = False):
        pass

    def is_here(self, table_name: str, identifier: str = "") -> bool:
        try:
            result = self.lookup(table_name, identifier, is_here=True)
            return len(result) > 0
        except Exception as e:
            bot_logger.success(f"Table {table_name} does not exist: {e}")
            return False

    @abstractmethod
    def modify(self, table_name: str, identifier: str, items: Dict[str, Any]):
        pass


class SQLDataUtilInterface(DataUtilInterface):
    def add(self, table_name: str, data_object: Dict[str, Any]):
        cleaned_data = {}
        for key, value in data_object.items():
            if key.startswith("_key."):
                new_key = key[len("_key."):]
                cleaned_data[new_key] = value
            else:
                cleaned_data[key] = value
        keys = ', '.join(cleaned_data.keys())
        placeholders = ', '.join('%s' for _ in cleaned_data.values())
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"
        try:
            self._execute_query(sql, tuple(cleaned_data.values()))
        except Exception as e:
            bot_logger.error(f"Error adding data to {table_name}: {e}")

    def delete(self, table_name: str, identifier: str):
        identifier_key, identifier_value = identifier.split("_", 1)
        sql = f"DELETE FROM {table_name} WHERE {identifier_key} = %s"
        try:
            self._execute_query(sql, (identifier_value,))
        except Exception as e:
            bot_logger.error(f"Error deleting data from {table_name}: {e}")

    @staticmethod
    def _get_results(columns: List[str], original_results: Union[tuple[tuple[Any, ...], ...], list]):
        return [{column: result[columns.index(column)] for column in columns} for result in original_results]

    def lookup(self, table_name: str, identifier: str = "", is_here: bool = False):
        if identifier:
            identifier_key, identifier_value = identifier.split("_", 1)
            sql = f'SELECT * FROM {table_name} WHERE {identifier_key} = %s'
            params = (identifier_value,)
        else:
            sql = f'SELECT * FROM {table_name}'
            params = ()
        try:
            cursor = self._execute_query(sql, params)
            results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return self._get_results(columns, results)
        except Exception as e:
            if not is_here:
                bot_logger.error(f"Error looking up data from {table_name}: {e}")
            raise

    def modify(self, table_name: str, identifier: str, items: Dict[str, Any]):
        identifier_key, identifier_value = identifier.split("_", 1)
        keys_values = ', '.join(f"{key} = %s" for key in items.keys())
        sql = f"UPDATE {table_name} SET {keys_values} WHERE {identifier_key} = %s"
        params = tuple(items.values()) + (identifier_value,)
        try:
            self._execute_query(sql, params)
        except Exception as e:
            bot_logger.error(f"Error modifying data from {table_name}: {e}")

    @abstractmethod
    def _connect(self, table_name: str = ""):
        pass

    @abstractmethod
    def _execute_query(self, query: str, params: tuple = ()):
        pass

    @abstractmethod
    def initialize(self, table_name: str, table_columns: List[Tuple[str, str, bool]]):
        pass


class FileDataUtilInterface(DataUtilInterface):
    @abstractmethod
    def _open_table(self, table_name: str) -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def initialize(table_name: str):
        pass

    @abstractmethod
    def _loop_search(self, table: Dict[str, Any], identifier: str = ""):
        pass

    @abstractmethod
    def lookup(self, table_name: str, identifier: str = "", search: bool = False, is_here: bool = False):
        pass
