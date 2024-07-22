from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import turned_off
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="开关·开启机器人",
    description="在本群开启机器人",
    usage=""
)

turn_on = on_alconna(
    Alconna("on"),
    priority=1,
    use_cmd_start=True,
    block=False
)


@turn_on.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if str(event.group_id) in turned_off.turned_off:
        datautil.delete("turned_off", f"groupid_{event.group_id}")
        turned_off.update()
        await turn_on.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 已在本群开启机器人")
        ]))
    else:
        await turn_on.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 机器人已经在本群开启了！")
        ]))
