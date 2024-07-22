import datetime

from arclet.alconna import Alconna
from nonebot import Bot
from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent, MessageSegment
from nonebot.internal.params import Arg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type
from nonebot_plugin_alconna import on_alconna

import constants
import message_records

__plugin_meta__ = PluginMetadata(
    name="回复私聊消息",
    description="回复上一条私聊消息",
    usage=""
)

reply = on_alconna(
    Alconna("reply"),
    use_cmd_start=True,
    permission=SUPERUSER,
    rule=is_type(PrivateMessageEvent)
)

cancel = constants.BotConstants.command_prefix + "cancel"
time_now = 0


@reply.handle()
async def handle_function():
    global time_now
    time_now = datetime.datetime.now().timestamp()
    if message_records.from_id == 0:
        await reply.finish("没有找到上一条消息的来源！")
    await reply.skip()


@reply.got("message", prompt=f"请输入要回复的内容！（若要取消回复，请在聊天框中输入{cancel}）")
async def got_message(bot: Bot, message: Message = Arg()):
    if (datetime.datetime.now().timestamp() - time_now) >= 45:
        await reply.finish("操作超时，已自动取消！")
    elif message.extract_plain_text() == cancel:
        await reply.finish("已取消回复消息！")
    else:
        await reply.send(f"已尝试将消息回复给 {message_records.from_id}")
        await bot.send_private_msg(user_id=message_records.from_id,
                                   message=MessageSegment.reply(message_records.message_id) + message)
