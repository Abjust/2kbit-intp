from textwrap import dedent
from typing import List, Tuple

import pymysql
from pymysql import Connection
from pymysql.cursors import Cursor

from codeintp.bot_utils.datautil.interface import SQLDataUtilInterface
from codeintp.bot_utils.logger import bot_logger


class MySQLDataUtil(SQLDataUtilInterface):
    def __init__(self, const):
        self.const = const

    def _connect(self, table_name: str = "") -> Connection:
        try:
            return pymysql.connect(
                host=self.const.db_host,
                port=self.const.db_port,
                user=self.const.db_user,
                password=self.const.db_password,
                database=self.const.db_name
            )
        except Exception as e:
            bot_logger.error(f"Error connecting: {e}")

    def _execute_query(self, query: str, params: tuple = ()) -> Cursor:
        try:
            with self._connect() as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(query, params)
                mydb.commit()
                return mycursor
        except pymysql.MySQLError as e:
            bot_logger.error(f"Error executing query: {e}")

    def initialize(self, table_name, table_columns: List[Tuple[str, str, bool]]):
        sql = dedent(f"""
                        create table if not exists {table_name} (
                        `id` int not null auto_increment,
                        """)
        unique_key = ""
        columns = []
        for column_name, column_type, is_unique in table_columns:
            if is_unique:
                unique_key = column_name
            columns.append(f"`{column_name}` {column_type}")
        if unique_key:
            columns.append(f"unique (`{unique_key}`)")
        columns.append("primary key (id)")
        sql += ", ".join(columns) + ");"
        try:
            self._execute_query(sql)
        except Exception as e:
            bot_logger.error(f"Error initializing a table: {e}")
