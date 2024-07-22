import datetime

from arclet.alconna import Alconna
from nonebot import Bot
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, MessageSegment
from nonebot.internal.params import Arg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

import constants

__plugin_meta__ = PluginMetadata(
    name="公告",
    description="发送跨群公告（广播）",
    usage=""
)

announce = on_alconna(
    Alconna("announce"),
    permission=SUPERUSER,
    use_cmd_start=True,
    priority=10
)

cancel = constants.BotConstants.command_prefix + "cancel"
time_now = 0


@announce.handle()
async def handle_function():
    global time_now
    time_now = datetime.datetime.now().timestamp()
    await announce.skip()


@announce.got("message", prompt=f"请输入要公告的内容！（若要取消，请输入{cancel}）")
async def got_message(bot: Bot, event: GroupMessageEvent, message: Message = Arg()):
    if (datetime.datetime.now().timestamp() - time_now) >= 45:
        await announce.finish((Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 操作超时，已自动取消！")
        ])))
    if message.extract_plain_text() == cancel:
        await announce.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 已取消发送消息！")
        ]))
    else:
        await announce.send(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 已尝试将指定消息发送到所有群！")
        ]))
        groups = await bot.get_group_list()
        for group in groups:
            await bot.send_group_msg(group_id=group['group_id'], message=message)
