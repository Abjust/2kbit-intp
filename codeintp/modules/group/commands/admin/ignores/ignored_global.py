from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission

__plugin_meta__ = PluginMetadata(
    name="群管·列举全局灰名单",
    description="列举出所有全局被加灰的人",
    usage=""
)

ignored_global = on_alconna(
    Alconna("ignoredg"),
    priority=10,
    use_cmd_start=True
)


@ignored_global.handle()
async def handle_function(event: GroupMessageEvent):
    ops = [permission.cache["ignored"][x] for x in range(len(permission.cache["ignored"]))]
    qualified = [y for x in ops for y in x if "0" in x[y]['groups']]
    if len(qualified) > 0:
        await ignored_global.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f"\n全局灰名单：{str(qualified)}")
        ]))
    else:
        await ignored_global.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 当前还没有设置全局灰名单")
        ]))
