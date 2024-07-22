from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="查看机器人帮助",
    usage=""
)

bot_help = on_alconna(
    Alconna("help"),
    use_cmd_start=True,
    priority=10
)


@bot_help.handle()
async def handle_function(event: GroupMessageEvent):
    await bot_help.finish(Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.at(event.sender.user_id),
        MessageSegment.text(" 请前往 https://2kbit.o0o.icu 查看 2kbit Code: INTP 使用教程！（尚未完工）")
    ]))
