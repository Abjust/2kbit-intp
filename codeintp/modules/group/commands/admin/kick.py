from typing import Any

from arclet.alconna import Alconna, Arg, Arparma
from nonebot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission
from codeintp.bot_utils.identify import identify

__plugin_meta__ = PluginMetadata(
    name="群管·踢人",
    description="从本群踢出某个人",
    usage=""
)

kick = on_alconna(
    Alconna("kick", Arg("target", Any)),
    priority=10,
    use_cmd_start=True
)


@kick.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent, result: Arparma):
    target = str(identify(result.query("target")).strip())
    is_valid = target.isdigit()
    compared = permission.compare(str(event.sender.user_id), target, str(event.group_id))
    is_higher = compared[0] > compared[1]
    has_permission = compared[0] >= 1
    if is_valid and has_permission and is_higher:
        await kick.send(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 已尝试踢出 {target}")
        ]))
        await bot.set_group_kick(group_id=event.group_id, user_id=target)
    elif not has_permission:
        await kick.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法踢出 {target}：宁踏马有权限吗？（恼）")
        ]))
    elif not is_higher:
        await kick.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法踢出 {target}：权限与目标相等或者比目标低")
        ]))
    elif not is_valid:
        await kick.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法踢出 {target}：宁这是数字吗？（恼）")
        ]))
