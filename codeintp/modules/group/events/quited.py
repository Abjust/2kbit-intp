from nonebot import on_notice, Bot
from nonebot.adapters.onebot.v11 import GroupDecreaseNoticeEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

__plugin_meta__ = PluginMetadata(
    name="有人退群事件",
    description="发悲报",
    usage=""
)

joined = on_notice(is_type(GroupDecreaseNoticeEvent))


@joined.handle()
async def handle_function(bot: Bot, event: GroupDecreaseNoticeEvent):
    if event.sub_type == "leave":
        await bot.send_group_msg(group_id=event.group_id, message=f"{event.user_id} 退群力（悲）")
