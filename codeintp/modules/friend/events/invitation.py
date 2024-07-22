from nonebot import on_request, Bot
from nonebot.adapters.onebot.v11 import GroupRequestEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

import constants

__plugin_meta__ = PluginMetadata(
    name="邀请进群事件",
    description="自动通过所有来自主人的请求，并自动拒绝其他人的请求",
    usage=""
)

invitation = on_request(is_type(GroupRequestEvent))


@invitation.handle()
async def handle_function(bot: Bot, event: GroupRequestEvent):
    if event.sub_type == "invite" and event.user_id == constants.BotConstants.owner_qq:
        await event.approve(bot=bot)
