from arclet.alconna import Alconna
from nonebot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.internal.params import Arg, ArgPlainText
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="生成消息串",
    description="仅仅是为了好玩",
    usage=""
)

mkmsg = on_alconna(
    Alconna("mkmsg"),
    priority=10,
    use_cmd_start=True
)
yes = [
    "yes",
    "y",
    "是"
]


@mkmsg.got("from_qq", "请输入消息发送者的qq号：")
@mkmsg.got("message", "请输入消息内容：")
@mkmsg.got("next_round", "还要继续吗？")
async def got_message(state: T_State, bot: Bot, event: GroupMessageEvent,
                      from_qq: Message = ArgPlainText(), message: Message = Arg(),
                      next_round: Message = ArgPlainText()):
    message_pair = (from_qq, str(message))
    message_pairs = state.get("message_pairs", [message_pair])
    total_rounds = state.get("total_rounds", 1)
    if not str(from_qq).isdigit():
        await mkmsg.reject("请重新输入qq号！")
    if next_round in yes and total_rounds < 5:
        state['total_rounds'] = total_rounds + 1
    elif next_round in yes and total_rounds >= 5:
        await mkmsg.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 轮数已达到上限，正在生成消息串……")
        ]))
    else:
        await mkmsg.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 正在生成消息串……")
        ]))
