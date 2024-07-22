from textwrap import dedent

from arclet.alconna import Alconna, Arg, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="定时广播·查看定时任务",
    description="查看定时广播任务",
    usage=""
)

lookup_schedule = on_alconna(
    Alconna("lookup_schedule", Arg("taskid", int)),
    priority=10,
    use_cmd_start=True
)


@lookup_schedule.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("schedules", f"taskid_{result.query('taskid')}"):
        task = datautil.lookup("schedules", f"taskid_{result.query('taskid')}")[0]
        message_chain = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(dedent(f"""
            任务ID：{task['taskid']}
            广播范围：{"全局" if task['scope'] == "all" else task['scope']}
            广播时间：{task['time']}
            是否启用：{bool(task['enabled'])}
            广播内容：
            """).rstrip()),
            MessageSegment.text("\n")])
        message_chain += Message(task['message'])
        await lookup_schedule.finish(message_chain)
    else:
        await lookup_schedule.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 找不到该任务！")
        ]))
