from arclet.alconna import Alconna, Arg, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission, scheduler
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="定时广播·删除定时任务",
    description="删除定时广播任务",
    usage=""
)

delete_schedule = on_alconna(
    Alconna("delete_schedule", Arg("taskid", int)),
    priority=10,
    use_cmd_start=True
)


@delete_schedule.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("schedules", f"taskid_{result.query('taskid')}"):
        task = datautil.lookup("schedules", f"taskid_{result.query('taskid')}")[0]
        has_permission = (permission.is_global_admin(str(event.sender.user_id)) if task["scope"] == "all"
                          else permission.is_group_admin(str(event.sender.user_id), task["scope"]))
        if has_permission:
            datautil.delete("schedules", f"taskid_{result.query('taskid')}")
            scheduler.update_schedules("remove", {"taskid": result.query('taskid')})
            await delete_schedule.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 已删除该任务！")
            ]))
        else:
            await delete_schedule.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 权限不足！")
            ]))
    else:
        await delete_schedule.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 找不到该任务！")
        ]))
