from nonebot import on_notice, Bot
from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent, MessageSegment, Message
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

__plugin_meta__ = PluginMetadata(
    name="有人加群事件",
    description="发喜报",
    usage=""
)

joined = on_notice(is_type(GroupIncreaseNoticeEvent))


@joined.handle()
async def handle_function(bot: Bot, event: GroupIncreaseNoticeEvent):
    await bot.send_group_msg(group_id=event.group_id, message=Message([
        MessageSegment.at(event.user_id),
        MessageSegment.text(" 来辣，让我们一起撅新人！（bushi")
    ]))
