import datetime
import random
from math import floor

import opencc
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·敲木鱼",
    description="敲电子木鱼，见机甲佛祖，取赛博真经",
    usage=""
)

hit = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("敲木鱼")),
    priority=10
)


@hit.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("woodenfish", f"playerid_{event.sender.user_id}"):
        time_now = datetime.datetime.now().timestamp()
        obj = datautil.lookup("woodenfish", f"playerid_{event.sender.user_id}")
        if obj["ban"] == 0:
            add = [1, 4, 5]
            r = random.randrange(0, len(add))
            if time_now - obj["end_time"] <= 3:
                modified_data = {
                    "hit_count": obj["hit_count"] + 1
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                hit_count = obj["hit_count"] + 1
                end_time = obj["end_time"]
            else:
                modified_data = {
                    "hit_count": 1,
                    "end_time": time_now
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                hit_count = 1
                end_time = time_now
            if (time_now - end_time <= 3 and hit_count > 5) and obj["total_ban"] < 4:
                modified_data = {
                    "ban": 2,
                    "hit_count": 0,
                    "total_ban": obj["total_ban"] + 1,
                    "gongde": floor(obj["gongde"] * 0.5),
                    "ee": obj["ee"] * 0.5,
                    "e": obj["e"] * 0.5,
                    "dt": time_now + 5400
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                await hit.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(" DoS佛祖是吧？这就给你封了（恼）（你被封禁 90 分钟，功德扣掉 50%）")
                ]))
            elif (time_now - end_time <= 3 and hit_count > 5) and obj["total_ban"] == 4:
                modified_data = {
                    "ban": 1,
                    "hit_count": 0,
                    "total_ban": 5,
                    "gongde": 0,
                    "ee": 0,
                    "e": 0,
                    "level": 1,
                    "nirvana": 1
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                await hit.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(" 多次DoS佛祖，死不悔改，罪不可赦（恼）（你被永久封禁，等级、涅槃值重置，功德清零）")
                ]))
            else:
                modified_data = {
                    "gongde": obj["gongde"] + add[r]
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                await hit.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(f" 功德 +{add[r]}")
                ]))
        else:
            await hit.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 敲拟吗呢？宁踏马被佛祖封号辣（恼）")
            ]))
    else:
        await hit.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 宁踏马害没注册？快发送“给我木鱼”注册罢！")
        ]))
