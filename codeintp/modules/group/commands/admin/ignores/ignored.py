from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission

__plugin_meta__ = PluginMetadata(
    name="群管·列举本群灰名单",
    description="列举出所有本群被加灰的人",
    usage=""
)

ignored = on_alconna(
    Alconna("ignored"),
    priority=10,
    use_cmd_start=True
)


@ignored.handle()
async def handle_function(event: GroupMessageEvent):
    ops = [permission.cache["ignored"][x] for x in range(len(permission.cache["ignored"]))]
    qualified = [y for x in ops for y in x if str(event.group_id) in x[y]['groups']]
    if len(qualified) > 0:
        await ignored.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f"\n本群灰名单：{str(qualified)}")
        ]))
    else:
        await ignored.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 本群还没有设置灰名单！")
        ]))
