import datetime
from typing import Any

from arclet.alconna import Alconna, Arg, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.identify import identify

__plugin_meta__ = PluginMetadata(
    name="叫人",
    description="呼叫某个在群里的人",
    usage=""
)

call = on_alconna(
    Alconna("call", Arg("target", Any), Arg("repetition", int, 3)),
    priority=10,
    use_cmd_start=True
)

called = []
call_cd = 40


@call.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    global called
    time_now = datetime.datetime.now().timestamp()
    target = str(identify(result.query("target")).strip())
    is_valid = target.isdigit()
    repetition = 1 if result.query("repetition") <= 0 else result.query("repetition")
    repetition = 10 if result.query("repetition") >= 10 else repetition
    selected = []
    if is_valid:
        is_here = False
        for x in called:
            if x[0] == event.group_id:
                selected = x
                is_here = True
                break
        if not is_here:
            called.append([event.group_id, 0])
            selected = [event.group_id, 0]

        if time_now - selected[1] >= call_cd:
            for _ in range(repetition):
                await call.send(Message([
                    MessageSegment.at(target),
                    MessageSegment.text(" 机器人正在呼叫你")
                ]))
            called[called.index(selected)][1] = time_now
        else:
            await call.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" CD未到，请别急！CD还剩： "
                                    f"{round(call_cd - (time_now - called[called.index(selected)][1]))} 秒")
            ]))
    else:
        await call.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 参数有误！")
        ]))
