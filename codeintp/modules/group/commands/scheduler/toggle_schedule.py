from arclet.alconna import Alconna, Arparma, Args
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils import permission, scheduler
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="定时广播·开关定时任务",
    description="开关定时广播任务",
    usage=""
)

toggle_schedule = on_alconna(
    Alconna("toggle_schedule", Args["taskid", int]["enabled", bool]),
    priority=10,
    use_cmd_start=True
)


@toggle_schedule.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("schedules", f"taskid_{result.query('taskid')}"):
        task = datautil.lookup("schedules", f"taskid_{result.query('taskid')}")[0]
        has_permission = (permission.is_global_admin(str(event.sender.user_id)) if task["scope"] == "all"
                          else permission.is_group_admin(str(event.sender.user_id), task["scope"]))
        current_status = task["enabled"]
        new_status = "开启" if result.query("enabled") else "关闭"
        if has_permission and (bool(current_status) != result.query("enabled")):
            modified_data = {
                "enabled": result.query("enabled")
            }
            datautil.modify("schedules", f"taskid_{result.query('taskid')}", modified_data)
            info = {
                "_key.taskid": task['taskid'],
                "scope": task['scope'],
                "message": task['message']
            }
            if new_status == "开启":
                scheduler.update_schedules("resume", info)
            else:
                scheduler.update_schedules("pause", info)
            await toggle_schedule.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(f" 已{new_status}该任务！")
            ]))
        elif not has_permission:
            await toggle_schedule.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 权限不足！")
            ]))
        elif bool(current_status) == result.query("enabled"):
            await toggle_schedule.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 新状态不能和原来的一样！")
            ]))

    else:
        await toggle_schedule.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 找不到该任务！")
        ]))
