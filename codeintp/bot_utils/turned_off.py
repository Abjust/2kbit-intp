import constants
from codeintp.bot_utils.datautil import factory

turned_off = []


def initialize():
    if not turned_off:
        update()


def update():
    datautil = factory.DataUtilFactory.create_data_util()
    exists = datautil.is_here("turned_off")
    is_sql = constants.BotConstants.db_type in ["mysql", "sqlite"]
    table_data = datautil.lookup("turned_off")
    if exists and is_sql:
        for item in table_data:
            turned_off.append(item['groupid'])
    elif exists and not is_sql:
        for item in table_data:
            turned_off.append(item)
