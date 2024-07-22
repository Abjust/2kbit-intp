from arclet.alconna import Alconna, Arg, Arparma
from nonebot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="群管·禁言自己",
    description="只是为了好玩",
    usage=""
)

mute_me = on_alconna(
    Alconna("muteme", Arg("minutes", int, 10)),
    priority=10,
    use_cmd_start=True
)


@mute_me.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent, result: Arparma):
    if 1 <= result.query("minutes") <= 43199:
        await mute_me.send(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 已尝试禁言 {event.sender.user_id}：{result.query('minutes')} 分钟")
        ]))
        await bot.set_group_ban(group_id=event.group_id, user_id=event.sender.user_id,
                                duration=result.query("minutes") * 60)
    else:
        await mute_me.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 无法禁言 {event.sender.user_id}：时长不正确")
        ]))
