from typing import Union

import constants
from codeintp.bot_utils.datautil.impl.json_impl import JSONDataUtil
from codeintp.bot_utils.datautil.impl.mysql_impl import MySQLDataUtil
from codeintp.bot_utils.datautil.impl.sqlite_impl import SQLiteDataUtil
from codeintp.bot_utils.datautil.impl.yaml_impl import YAMLDataUtil
from codeintp.bot_utils.datautil.interface import SQLDataUtilInterface, FileDataUtilInterface


class DataUtilFactory:
    @staticmethod
    def create_data_util() -> Union[SQLDataUtilInterface, FileDataUtilInterface]:
        db_type = constants.BotConstants.db_type
        if db_type == 'mysql':
            return MySQLDataUtil(constants.BotConstants)
        elif db_type == 'sqlite':
            return SQLiteDataUtil()
        elif db_type == 'json':
            return JSONDataUtil()
        elif db_type == 'yaml':
            return YAMLDataUtil()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
