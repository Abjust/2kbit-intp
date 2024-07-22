import os
import sqlite3
from sqlite3 import Cursor
from textwrap import dedent
from typing import List, Tuple

from codeintp.bot_utils.datautil.interface import SQLDataUtilInterface
from codeintp.bot_utils.logger import bot_logger


class SQLiteDataUtil(SQLDataUtilInterface):
    def _connect(self, table_name: str = ""):
        try:
            return sqlite3.connect(f"data/{table_name}.db")
        except Exception as e:
            bot_logger.error(f"Error connecting: {e}")
            raise

    def _execute_query(self, query: str, params: tuple = ()) -> Cursor:
        try:
            with self._connect() as db:
                cursor = db.cursor()
                cursor.execute(query, params)
                db.commit()
                return cursor
        except Exception as e:
            bot_logger.error(f"Error executing query: {e}")
            raise

    def initialize(self, table_name: str, table_columns: List[Tuple[str, str, bool]]):
        os.makedirs("data", exist_ok=True)
        sql = dedent(f"""
                        create table if not exists {table_name} (
                        """)
        unique_key = ""
        columns = []
        for column_name, column_type, is_unique in table_columns:
            if is_unique:
                unique_key = column_name
            columns.append(f"`{column_name}` {column_type}")
        if unique_key:
            columns.append(f"unique (`{unique_key}`)")
        sql += ", ".join(columns) + ");"
        try:
            self._execute_query(sql)
        except Exception as e:
            bot_logger.error(f"Error initializing a table: {e}")
