import datetime

from arclet.alconna import Alconna, Args, Arparma
from nonebot import Bot
from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent
from nonebot.internal.params import Arg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type
from nonebot_plugin_alconna import on_alconna

import constants

__plugin_meta__ = PluginMetadata(
    name="发送私聊消息",
    description="主动发送私聊消息",
    usage=""
)

send = on_alconna(
    Alconna("send", Args["target", int]),
    use_cmd_start=True,
    permission=SUPERUSER,
    rule=is_type(PrivateMessageEvent)
)

cancel = constants.BotConstants.command_prefix + "cancel"
time_now = 0


@send.handle()
async def handle_function():
    global time_now
    time_now = datetime.datetime.now().timestamp()
    await send.skip()


@send.got("message", prompt=f"请输入要发送的内容！（若要取消发送，请在聊天框中输入{cancel}）")
async def got_message(bot: Bot, result: Arparma, message: Message = Arg()):
    if (datetime.datetime.now().timestamp() - time_now) >= 45:
        await send.finish("操作超时，已自动取消！")
    if message.extract_plain_text() == cancel:
        await send.finish("已取消发送消息！")
    else:
        await send.send(f"已尝试将消息发送给 {result.query('target')}")
        await bot.send_private_msg(user_id=result.query('target'), message=message)
