import random
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
    name="定时广播·新建定时任务",
    description="新建定时广播任务",
    usage=""
)

add_schedule = on_alconna(
    Alconna("add_schedule",
            Subcommand(
                "this",
                Arg("time", str)
            ),
            Subcommand(
                "all",
                Arg("time", str)
            )),
    priority=10,
    use_cmd_start=True
)

cancel = constants.BotConstants.command_prefix + "cancel"


@add_schedule.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    has_permission = permission.is_group_admin(str(event.sender.user_id), str(event.group_id)) if result.find("this") \
        else permission.is_global_admin(str(event.sender.user_id))
    scope = str(event.group_id) if list(result.subcommands.keys())[0] == "this" else "all"
    all_tasks = datautil.lookup("schedules", f"scope_{scope}", True)
    if has_permission:
        try:
            datetime.strptime(result.query("time"), '%H:%M')
            repeated = len([x for x in all_tasks if x['time'] == result.query("time")]) > 0
            if repeated:
                await add_schedule.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text(" 新建失败：在同一范围内存在有同一执行时间的定时任务！")
                ]))
        except ValueError:
            await add_schedule.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 新建失败：时间格式有误！")
            ]))
    else:
        await add_schedule.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 新建失败：权限不足！")
        ]))


@add_schedule.got("message", prompt=f"请输入要定时广播的内容！（若要取消，请输入{cancel}）")
async def got_message(time: str, event: GroupMessageEvent, result: Arparma, message: Message = NoneBotArg()):
    datautil = factory.DataUtilFactory.create_data_util()
    scope_name = "本群" if list(result.subcommands.keys())[0] == "this" else "全局"
    scope = str(event.group_id) if list(result.subcommands.keys())[0] == "this" else "all"
    if message.extract_plain_text() == cancel:
        await add_schedule.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 已取消新建定时任务！")
        ]))
    else:
        columns = [
            ("taskid", "int", True),
            ("scope", "varchar(16)", False),
            ("time", "varchar(16)", False),
            ("message", "text", False),
            ("enabled", "boolean", False),
        ]
        datautil.initialize("schedules", columns)
        r = random.randint(100000, 999999)
        if datautil.is_here("schedules", f"taskid_{r}"):
            while datautil.is_here("schedules", f"taskid_{r}"):
                r = random.randint(100000, 999999)
        obj = {
            "_key.taskid": r,
            "scope": scope,
            "time": time,
            "message": str(message),
            "enabled": True
        }
        datautil.add("schedules", obj)
        message_chain = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 已新建{scope_name}定时广播任务，其ID为{r}，将于每天{time}执行，内容如下：\n")])
        message_chain += message
        scheduler.update_schedules("add", obj)
        await add_schedule.finish(message_chain)
