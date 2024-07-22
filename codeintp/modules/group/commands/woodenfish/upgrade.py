import math

import opencc
from arclet.alconna import Alconna, Arg, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·升级木鱼",
    description="让赛博木鱼变得更强",
    usage=""
)

upgrade = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("升级木鱼"), Arg("level", int, 1)),
    priority=10
)


@upgrade.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("woodenfish", f"playerid_{event.sender.user_id}"):
        obj = datautil.lookup("woodenfish", f"playerid_{event.sender.user_id}")
        if result.query("level") > 0 and obj["ban"] == 0:
            needed_e = obj["level"] + 2 + result.query("level")
            sufficient_ee = pow(10, obj["ee"]) + obj["e"] >= needed_e
            sufficient_e = obj["e"] >= needed_e
            if sufficient_e:
                modified_data = {
                    "e": obj["e"] - needed_e,
                    "level": obj["level"] + result.query("level")
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                await upgrade.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text(" 木鱼升级成功辣（喜）")
                ]))
            elif sufficient_ee:
                modified_data = {
                    "ee": math.log10((pow(10, obj["ee"]) + obj["e"]) - needed_e),
                    "e": 0,
                    "level": obj["level"] + result.query("level")
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                await upgrade.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text(" 木鱼升级成功辣（喜）")
                ]))
            else:
                await upgrade.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text(" 升级个毛啊？宁踏马功德不够（恼）")
                ]))
        elif obj["ban"] != 0:
            await upgrade.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 升级个毛啊？宁踏马被佛祖封号辣（恼）")
            ]))
        elif result.query("level") <= 0:
            await upgrade.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 升级个毛啊？宁这数字踏马怎么让我理解？（恼）")
            ]))
    else:
        await upgrade.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 宁踏马害没注册？快发送“给我木鱼”注册罢！")
        ]))
