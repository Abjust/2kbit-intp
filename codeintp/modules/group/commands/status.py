import datetime
import platform
import time

import cpuinfo
import psutil
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="运行状态",
    description="获取2kbit Code: INTP运行状态",
    usage=""
)

import constants

status = on_alconna(
    Alconna("status"),
    priority=10,
    use_cmd_start=True
)


@status.handle()
async def handle_function(event: GroupMessageEvent):
    time_now = datetime.datetime.now().timestamp()
    time_elapsed = round(time_now - constants.BotConstants.boot_time, 2)
    time_elapsed_formatted = time.strftime('%H:%M:%S', time.gmtime(time_elapsed))
    await status.finish(Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.at(event.sender.user_id),
        MessageSegment.text("\n"),
        MessageSegment.text("机器人运行信息\n"
                            f"运行环境版本：Python {platform.python_version()}\n"
                            f"系统版本：{platform.uname().system} {platform.uname().version}\n"
                            f"CPU：{cpuinfo.get_cpu_info()['brand_raw']} （占用率 {psutil.cpu_percent()} %）\n"
                            f"剩余RAM：{psutil.virtual_memory().free / 1048576:.2f} / "
                            f"{psutil.virtual_memory().total / 1048576:.2f} MB\n"
                            f"剩余Swap：{psutil.swap_memory().free / 1048576:.2f} / "
                            f"{psutil.swap_memory().total / 1048576:.2f} MB\n"
                            f"剩余存储空间：{psutil.disk_usage('/').free / 1073741824:.2f} / "
                            f"{psutil.disk_usage('/').total / 1073741824:.2f} GB\n"
                            f"机器人已运行：{time_elapsed_formatted}")
    ]))
