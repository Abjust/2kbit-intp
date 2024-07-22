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

mute = on_alconna(
    Alconna("mute", Arg("target", Any), Arg("minutes", int, 10)),
    priority=10,
    use_cmd_start=True
)


@mute.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent, result: Arparma):
    target = str(identify(result.query("target")).strip())
    is_valid = target.isdigit()
    compared = permission.compare(str(event.sender.user_id), target, str(event.group_id))
    is_higher = compared[0] > compared[1]
    has_permission = compared[0] >= 1
    if is_valid and has_permission and is_higher:
        if 1 <= result.query("minutes") <= 43199:
            await mute.send(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(f" 已尝试禁言 {target}：{result.query('minutes')} 分钟")
            ]))
            await bot.set_group_ban(group_id=event.group_id, user_id=target,
                                    duration=result.query("minutes") * 60)
        else:
            await mute.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(f" 无法禁言 {target}：时长不正确")
            ]))
    elif not has_permission:
        await mute.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法禁言 {target}：宁踏马有权限吗？（恼）")
        ]))
    elif not is_higher:
        await mute.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法禁言 {target}：权限与目标相等或者比目标低")
        ]))
    elif not is_valid:
        await mute.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法禁言 {target}：宁这是数字吗？（恼）")
        ]))
