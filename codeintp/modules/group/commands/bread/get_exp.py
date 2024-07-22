import datetime
import random

from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·获取经验",
    description="自动获取经验",
    usage=""
)

get_exp = on_message(is_type(GroupMessageEvent), priority=5, block=False)


@get_exp.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    time_now = datetime.datetime.now().timestamp()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        obj = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
        if time_now - obj["last_expgain"] >= 86400:
            modified_data = {
                "exp_gained_today": 0
            }
            datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
        obj = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
        maximum_exp = pow(2, obj["factory_level"] - 1)
        exp = 1 if maximum_exp == 1 else random.randint(1, maximum_exp)
        not_maxed = obj["exp_gained_today"] < 300 * maximum_exp
        if time_now - obj["last_expfull"] >= 86400 and not_maxed:
            gained_exp = exp \
                if exp + obj["exp_gained_today"] <= 300 * maximum_exp \
                else 300 * maximum_exp - obj["exp_gained_today"]
            modified_data = {
                "last_expgain": time_now,
                "factory_exp": obj["factory_exp"] + gained_exp,
                "exp_gained_today": obj["exp_gained_today"] + gained_exp
            }
            datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
        elif time_now - obj["last_expfull"] >= 86400 and not not_maxed:
            modified_data = {
                "last_expfull": obj["last_expgain"]
            }
            datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
            await get_exp.finish("本群已达到今日获取经验上限！")
