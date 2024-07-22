from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission

__plugin_meta__ = PluginMetadata(
    name="群管·列举全局管理",
    description="列举出所有全局机器人管理员",
    usage=""
)

list_op_global = on_alconna(
    Alconna("listopg"),
    priority=10,
    use_cmd_start=True
)


@list_op_global.handle()
async def handle_function(event: GroupMessageEvent):
    ops = [permission.cache["ops"][x] for x in range(len(permission.cache["ops"]))]
    qualified = [y for x in ops for y in x if "0" in x[y]['groups']]
    if len(qualified) > 0:
        await list_op_global.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f"\n当前全局机器人管理员：{str(qualified)}")
        ]))
    else:
        await list_op_global.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 当前还没有设置全局机器人管理员！")
        ]))
