import datetime

import opencc
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·给我木鱼",
    description="注册赛博木鱼账号",
    usage=""
)

register = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("给我木鱼")),
    priority=10
)


@register.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if not datautil.is_here("woodenfish", f"playerid_{event.sender.user_id}"):
        columns = [
            ["playerid", "varchar(16)", True],
            ["time", "bigint", False],
            ["level", "int", False],
            ["gongde", "int", False],
            ["e", "double", False],
            ["ee", "double", False],
            ["nirvana", "double", False],
            ["ban", "int", False],
            ["dt", "bigint", False],
            ["end_time", "bigint", False],
            ["hit_count", "int", False],
            ["info_time", "bigint", False],
            ["info_count", "int", False],
            ["info_ctrl", "bigint", False],
            ["total_ban", "int", False],
        ]
        datautil.initialize("woodenfish", columns)
        obj = {
            "_key.userid": f"{event.sender.user_id}",
            "time": datetime.datetime.now().timestamp(),
            "level": 1,
            "gongde": 0,
            "e": 0,
            "ee": 0,
            "nirvana": 1,
            "ban": 0,
            "dt": 946656000,
            "end_time": 946656000,
            "hit_count": 0,
            "info_time": 946656000,
            "info_count": 0,
            "info_ctrl": 946656000,
            "total_ban": 0
        }
        datautil.add("woodenfish", obj)
        await register.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 注册成功辣！")
        ]))
    else:
        await register.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 宁踏马不是注册过了吗？")
        ]))
