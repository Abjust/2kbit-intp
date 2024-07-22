from arclet.alconna import Alconna, Subcommand
from nonebot.adapters.onebot.v11 import MessageSegment, Message, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="测试",
    description="发送测试消息",
    usage=""
)

test = on_alconna(
    Alconna("test",
            Subcommand("1")),
    priority=10,
    use_cmd_start=True,
    use_cmd_sep=True
)


@test.handle()
async def handle_function(event: GroupMessageEvent):
    await test.finish(Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.at(event.sender.user_id),
        MessageSegment.text(" Hello World!")
    ]))
