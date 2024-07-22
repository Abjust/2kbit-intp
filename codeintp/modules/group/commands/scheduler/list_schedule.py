from textwrap import dedent

from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="定时广播·列举定时任务",
    description="列举出所有定时广播任务的任务ID",
    usage=""
)

list_schedule = on_alconna(
    Alconna("list_schedule"),
    priority=10,
    use_cmd_start=True
)


@list_schedule.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("schedules"):
        group_tasks = datautil.lookup("schedules", f"scope_{event.group_id}", True)
        group_tasks = [x['taskid'] for x in group_tasks]
        global_tasks = datautil.lookup("schedules", "scope_all", True)
        global_tasks = [x['taskid'] for x in global_tasks]
        await list_schedule.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(dedent(f"""
                            全局任务：{str(global_tasks)}
                            本群任务：{str(group_tasks)}
                            """).rstrip()),
            MessageSegment.text("\n")
        ]))
