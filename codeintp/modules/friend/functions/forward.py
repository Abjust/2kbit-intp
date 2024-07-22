from textwrap import dedent

from nonebot import on_message, Bot
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

import constants
import message_records

__plugin_meta__ = PluginMetadata(
    name="转发私聊消息",
    description="将别人发给机器人的私聊消息转发给主人",
    usage=""
)

forward = on_message(is_type(PrivateMessageEvent), priority=10)


@forward.handle()
async def handle_function(bot: Bot, event: PrivateMessageEvent):
    if event.sender.user_id != constants.BotConstants.owner_qq:
        await bot.send_private_msg(user_id=constants.BotConstants.owner_qq, message=dedent(f"""
        机器人收到了一条消息！
        来源：{event.sender.user_id}
        （消息内容见下方）
        """).strip())
        await bot.send_private_msg(user_id=constants.BotConstants.owner_qq, message=event.message)
        message_records.from_id = event.sender.user_id
        message_records.message_id = event.message_id
