from datetime import datetime

from arclet.alconna import Alconna, Subcommand, Arg, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.internal.params import Arg as NoneBotArg
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

import constants
from codeintp.bot_utils import permission, scheduler
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="定时广播·修改定时任务",
    description="修改定时广播任务",
    usage=""
)

modify_schedule = on_alconna(
    Alconna("modify_schedule", Arg("taskid", int),
            Subcommand("time", Arg("time", str)),
            Subcommand("message")),
    priority=10,
    use_cmd_start=True
)

cancel = constants.BotConstants.command_prefix + "cancel"


@modify_schedule.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("schedules", f"taskid_{result.query('taskid')}"):
        task = datautil.lookup("schedules", f"taskid_{result.query('taskid')}")[0]
        has_permission = (permission.is_global_admin(str(event.sender.user_id)) if task["scope"] == "all"
                          else permission.is_group_admin(str(event.sender.user_id), task["scope"]))
        if has_permission and result.find("time"):
            try:
                datetime.strptime(result.query("time"), '%H:%M')
                modified_data = {
                    "time": result.query("time")
                }
                datautil.modify("schedules", f"taskid_{result.query('taskid')}", modified_data)
                await modify_schedule.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text(f" 已修改该任务的执行时间！新的执行时间为：{result.query('time')}")
                ]))
            except ValueError:
                await modify_schedule.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text(" 时间格式有误！")
                ]))
        elif not has_permission:
            await modify_schedule.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 权限不足！")
            ]))

    else:
        await modify_schedule.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 找不到该任务！")
        ]))


@modify_schedule.got("message", prompt=f"请输入要定时广播的内容！（若要取消，请输入{cancel}）")
async def got_message(event: GroupMessageEvent, result: Arparma, message: Message = NoneBotArg()):
    datautil = factory.DataUtilFactory.create_data_util()
    modified_data = {
        "message": str(message)
    }
    datautil.modify("schedules", f"taskid_{result.query('taskid')}", modified_data)
    task = datautil.lookup("schedules", f"taskid_{result.query('taskid')}")[0]
    info = {
        "_key.taskid": task['taskid'],
        "scope": task['scope'],
        "message": task['message']
    }
    scheduler.update_schedules("modify", info)
    message_chain = Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.at(event.sender.user_id),
        MessageSegment.text(" 已修改该任务的广播内容！新的广播内容如下：\n")
    ])
    message_chain += message
    await modify_schedule.finish(message_chain)
