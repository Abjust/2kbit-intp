from nonebot.plugin import PluginMetadata

import constants
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="权限工具",
    description="提供有关权限的一些操作",
    usage=""
)

cache = {
    "ops": [],
    "blocklist": [],
    "ignored": []
}


# 初始化缓存表
def initialize_cache():
    if cache["ops"] == [] and cache["blocklist"] == [] and cache["ignored"] == []:
        obj = {f"{constants.BotConstants.bot_qq}": {
            "groups": ["0"]
        }}
        cache["ops"].append(obj)
        update_cache("ops")
        update_cache("blocklist")
        update_cache("ignored")


# 更新缓存表
def update_cache(table_name: str):
    datautil = factory.DataUtilFactory.create_data_util()
    exists = datautil.is_here(table_name)
    is_sql = constants.BotConstants.db_type in ["mysql", "sqlite"]
    cache["table_name"] = []
    if exists and is_sql:
        table_data = sorted(datautil.lookup(table_name), key=lambda x: x['userid'])
        data_indexes = set([x['userid'] for x in table_data])
        for item in data_indexes:
            groups = [x['groupid'] for x in table_data if x['userid'] == item]
            obj = {item: {
                "groups": groups
            }}
            if obj not in cache[table_name]:
                cache[table_name].append(obj)
    elif exists and not is_sql:
        table_data = datautil.lookup(table_name)
        if table_data not in cache[table_name]:
            cache[table_name].append(table_data)


# 判断是否是全局管理员
def is_global_admin(userid: str) -> bool:
    if cache["ops"]:
        ops = [cache["ops"][x] for x in range(len(cache["ops"]))]
        qualified = [y for x in ops for y in x if "0" in x[y]['groups']]
        return userid in qualified
    return False


# 判断是否是群管理员
def is_group_admin(userid: str, groupid: str) -> bool:
    if cache["ops"]:
        ops = [cache["ops"][x] for x in range(len(cache["ops"]))]
        qualified = [y for x in ops for y in x if groupid in x[y]['groups']]
        return userid in qualified or is_global_admin(userid)
    return False


# 判断是否被全局加黑
def is_global_blocked(userid: str) -> bool:
    if cache["blocklist"]:
        blocklist = [cache["blocklist"][x] for x in range(len(cache["blocklist"]))]
        qualified = [y for x in blocklist for y in x if "0" in x[y]['groups']]
        return userid in qualified
    return False


# 判断是否被本群加黑
def is_group_blocked(userid: str, groupid: str) -> bool:
    if cache["blocklist"]:
        blocklist = [cache["blocklist"][x] for x in range(len(cache["blocklist"]))]
        qualified = [y for x in blocklist for y in x if groupid in x[y]['groups']]
        return userid in qualified or is_global_blocked(userid)
    return False


# 判断是否被全局加灰
def is_global_ignored(userid: str) -> bool:
    if cache["ignored"]:
        ignored = [cache["ignored"][x] for x in range(len(cache["ignored"]))]
        qualified = [y for x in ignored for y in x if "0" in x[y]['groups']]
        return userid in qualified
    return False


# 判断是否被本群加灰
def is_group_ignored(userid: str, groupid: str) -> bool:
    if cache["ignored"]:
        ignored = [cache["ignored"][x] for x in range(len(cache["ignored"]))]
        qualified = [y for x in ignored for y in x if groupid in x[y]['groups']]
        return userid in qualified or is_global_ignored(userid)
    return False


# 比较权限
def compare(user1: str, user2: str, groupid: str) -> list[int]:
    permission_list = []
    # 第一个人
    if user1 == str(constants.BotConstants.owner_qq):
        permission_list.append(3)
    elif is_global_admin(user1):
        permission_list.append(2)
    elif is_group_admin(user1, groupid):
        permission_list.append(1)
    else:
        permission_list.append(0)
    # 第二个人
    if user2 == str(constants.BotConstants.owner_qq):
        permission_list.append(3)
    elif is_global_admin(user2):
        permission_list.append(2)
    elif is_group_admin(user2, groupid):
        permission_list.append(1)
    else:
        permission_list.append(0)
    return permission_list
