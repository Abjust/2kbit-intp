from math import trunc

import opencc
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·涅槃重生",
    description="功德圆满",
    usage=""
)

nirvana = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("涅槃重生")),
    priority=10
)


@nirvana.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("woodenfish", f"playerid_{event.sender.user_id}"):
        obj = datautil.lookup("woodenfish", f"playerid_{event.sender.user_id}")
        if obj["nirvana"] < 5:
            if obj["ban"] == 0:
                if obj["ee"] >= 10 + trunc((obj["nirvana"] - 1) / 0.05) * 1.5:
                    modified_data = {
                        "nirvana": trunc((obj["nirvana"] + 0.05) * 100) / 100,
                        "level": 1,
                        "ee": 0,
                        "e": 0,
                        "gongde": 0
                    }
                    datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                    await nirvana.finish(Message([
                        MessageSegment.reply(event.message_id),
                        MessageSegment.at(event.sender.user_id),
                        MessageSegment.text(" 涅槃重生，功德圆满（喜）")
                    ]))
                else:
                    await nirvana.finish(Message([
                        MessageSegment.reply(event.message_id),
                        MessageSegment.at(event.sender.user_id),
                        MessageSegment.text(" 涅槃重生个毛啊？宁踏马功德不够（恼）")
                    ]))
            else:
                await nirvana.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text(" 涅槃重生个毛啊？宁踏马被佛祖封号辣（恼）")
                ]))
        else:
            await nirvana.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 涅槃重生个毛啊？宁踏马已经不能涅槃重生辣（恼）")
            ]))
    else:
        await nirvana.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 宁踏马害没注册？快发送“给我木鱼”注册罢！")
        ]))
