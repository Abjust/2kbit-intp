from typing import Any

from arclet.alconna import Alconna, Arg, Arparma
from nonebot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission
from codeintp.bot_utils.identify import identify

__plugin_meta__ = PluginMetadata(
    name="群管·禁言",
    description="在本群禁言某个人",
    usage=""
)

unmute = on_alconna(
    Alconna("unmute", Arg("target", Any)),
    priority=10,
    use_cmd_start=True
)


@unmute.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent, result: Arparma):
    target = str(identify(result.query("target")).strip())
    is_valid = target.isdigit()
    compared = permission.compare(str(event.sender.user_id), target, str(event.group_id))
    has_permission = compared[0] >= 1
    if is_valid and has_permission:
        await unmute.send(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 已尝试解禁 {target}")
        ]))
        await bot.set_group_ban(group_id=event.group_id, user_id=target,
                                duration=0)
    elif not has_permission:
        await unmute.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法解禁 {target}：宁踏马有权限吗？（恼）")
        ]))
    elif not is_valid:
        await unmute.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法解禁 {target}：宁这是数字吗？（恼）")
        ]))
