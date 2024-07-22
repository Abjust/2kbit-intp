from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission

__plugin_meta__ = PluginMetadata(
    name="群管·列举本群管理",
    description="列举出所有本群的机器人管理员",
    usage=""
)

list_op = on_alconna(
    Alconna("listop"),
    priority=10,
    use_cmd_start=True
)


@list_op.handle()
async def handle_function(event: GroupMessageEvent):
    ops = [permission.cache["ops"][x] for x in range(len(permission.cache["ops"]))]
    qualified = [y for x in ops for y in x if str(event.group_id) in x[y]['groups']]
    if len(qualified) > 0:
        await list_op.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f"\n本群机器人管理员：{str(qualified)}")
        ]))
    else:
        await list_op.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 本群还没有设置机器人管理员！")
        ]))
