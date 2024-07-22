from nonebot import on_request, Bot
from nonebot.adapters.onebot.v11 import FriendRequestEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

__plugin_meta__ = PluginMetadata(
    name="加好友事件",
    description="自动同意加好友事件",
    usage=""
)

add_friend = on_request(is_type(FriendRequestEvent))


@add_friend.handle()
async def handle_function(bot: Bot, event: FriendRequestEvent):
    await event.approve(bot=bot)
