import random
from typing import Any

from arclet.alconna import Alconna, Arg, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

import constants
from codeintp.bot_utils import permission
from codeintp.bot_utils.datautil import factory
from codeintp.bot_utils.identify import identify

__plugin_meta__ = PluginMetadata(
    name="群管·本群加黑",
    description="将某个人加入到本群的黑名单",
    usage=""
)

block = on_alconna(
    Alconna("block", Arg("target", Any)),
    priority=10,
    use_cmd_start=True
)


@block.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    target = str(identify(result.query("target")).strip())
    is_valid = target.isdigit()
    in_blocklist = permission.is_group_blocked(identify(result.query("target")), str(event.group_id))
    compared = permission.compare(str(event.sender.user_id), target, str(event.group_id))
    is_higher = compared[0] > compared[1]
    has_permission = compared[0] >= 1
    if is_valid and has_permission and is_higher and not in_blocklist:
        columns = [
            ("recordid", "int", True),
            ("userid", "varchar(16)", False),
            ("groupid", "varchar(16)", False)
        ]
        datautil.initialize("blocklist", columns)
        # 分类讨论
        if constants.BotConstants.db_type in ["mysql", "sqlite"]:
            r = random.randint(100000, 999999)
            if datautil.is_here("blocklist", f"recordid_{r}"):
                while datautil.is_here("blocklist", f"recordid_{r}"):
                    r = random.randint(100000, 999999)
            obj = {
                "_key.recordid": r,
                "userid": target,
                "groupid": event.group_id
            }
            datautil.add("blocklist", obj)
        else:
            if not datautil.is_here("blocklist", f"userid_{target}"):
                obj = {
                    "_key.userid": target,
                    "groups": [str(event.group_id)]
                }
                datautil.add("blocklist", obj)
            else:
                obj1 = datautil.lookup("blocklist", f"userid_{target}")
                groups = obj1['groups']
                groups.append(str(event.group_id))
                modified_data = {
                    "groups": groups
                }
                datautil.modify("blocklist", f"userid_{target}", modified_data)
        permission.update_cache("blocklist")
        await block.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(f" 已将 {target} 加入到本群黑名单")
        ]))
    elif not has_permission:
        await block.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法加黑：宁踏马有权限吗？（恼）")
        ]))
    elif not is_higher:
        await block.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法加黑：权限与目标相等或者比目标低")
        ]))
    elif in_blocklist:
        await block.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法加黑：这个人已经被加黑了！")
        ]))
    elif not is_valid:
        await block.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法加黑：宁这是数字吗？（恼）")
        ]))
