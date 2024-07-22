import nonebot
from nonebot.adapters.onebot.v11 import Message
from nonebot_plugin_apscheduler import scheduler

from codeintp.bot_utils.datautil import factory

schedule_ids = []


# 生成消息对象
def create_message(message_str: str):
    return Message(message_str)


# 生成任务ID
def generate_task_id(task_id: str):
    return f"taskid_{task_id}"


# 群内定时广播
async def this_schedule(group_id: str, message: Message):
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=int(group_id), message=message)


# 跨群定时广播
async def all_schedule(message: Message):
    bot = nonebot.get_bot()
    groups = await bot.get_group_list()
    for group in groups:
        await bot.send_group_msg(group_id=group['group_id'], message=message)


# 添加任务
def add_task(task_info: dict):
    time = str(task_info["time"]).split(":")
    task_id = generate_task_id(task_info['_key.taskid'])
    message = create_message(task_info['message'])

    if task_info["scope"] == "all":
        scheduler.add_job(
            func=all_schedule,
            trigger="cron",
            hour=time[0],
            minute=time[1],
            id=task_id,
            args=[message]
        )
    else:
        scheduler.add_job(
            func=this_schedule,
            trigger="cron",
            hour=time[0],
            minute=time[1],
            id=task_id,
            args=[task_info['scope'], message]
        )


# 更新任务列表
def update_schedules(action: str, task_info=None):
    datautil = factory.DataUtilFactory.create_data_util()
    if task_info is None:
        task_info = {}
    schedules = datautil.lookup("schedules")
    if action == "initialize":
        for schedule in schedules:
            schedule_ids.append(schedule['taskid'])
            if schedule['enabled']:
                add_task({
                    "_key.taskid": schedule['taskid'],
                    "scope": schedule['scope'],
                    "time": schedule['time'],
                    "message": schedule['message']
                })
    elif action == "add":
        add_task(task_info)
    elif action == "remove":
        scheduler.remove_job(generate_task_id(task_info['taskid']))
    elif action == "modify":
        task_id = generate_task_id(task_info['taskid'])
        job = scheduler.get_job(task_id)
        if job:
            scheduler.modify_job(
                task_id,
                args=[create_message(task_info['message'])]
                if task_info['scope'] == "all"
                else [task_info['scope'], create_message(task_info['message'])]
            )
        elif task_info['taskid'] in schedule_ids:
            add_task(task_info)
    elif action == "reschedule":
        time = str(task_info["time"]).split(":")
        scheduler.reschedule_job(generate_task_id(task_info['taskid']), "cron", hour=time[0], minute=time[1])
    elif action == "pause":
        scheduler.pause_job(generate_task_id(task_info['taskid']))
    elif action == "resume":
        if task_info['taskid'] in schedule_ids:
            scheduler.resume_job(generate_task_id(task_info['taskid']))
        else:
            add_task(task_info)
