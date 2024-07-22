import opencc
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·撅佛祖",
    description="等着永封罢（恼）",
    usage=""
)

jue = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("撅佛祖")),
    priority=10
)


@jue.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("woodenfish", f"playerid_{event.sender.user_id}"):
        obj = datautil.lookup("woodenfish", f"playerid_{event.sender.user_id}")
        if obj["ban"] == 0:
            modified_data = {
                "ban": 1
            }
            datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
            await jue.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 敢撅佛祖？罪不可赦（恼）（你被永久封禁）")
            ]))
        else:
            await jue.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 撅拟吗呢？宁踏马被佛祖封号辣（恼）")
            ]))
    else:
        await jue.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 宁踏马害没注册？快发送“给我木鱼”注册罢！")
        ]))
