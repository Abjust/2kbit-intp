from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import turned_off
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="开关·关闭机器人",
    description="在本群关闭机器人",
    usage=""
)

turn_off = on_alconna(
    Alconna("off"),
    priority=10,
    use_cmd_start=True
)


@turn_off.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    columns = [
        ("groupid", "varchar(16)", True)
    ]
    datautil.initialize("turned_off", columns)
    obj = {
        "_key.groupid": str(event.group_id)
    }
    datautil.add("turned_off", obj)
    turned_off.update()
    await turn_off.finish(Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.at(event.sender.user_id),
        MessageSegment.text(" 已在本群关闭机器人")
    ]))
