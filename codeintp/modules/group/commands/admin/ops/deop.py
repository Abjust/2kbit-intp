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
    name="群管·本群下管",
    description="撤销某个人在本群的机器人管理员权限",
    usage=""
)

deop = on_alconna(
    Alconna("deop", Arg("target", Any)),
    priority=10,
    use_cmd_start=True
)


@deop.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    target = str(identify(result.query("target")).strip())
    is_valid = target.isdigit()
    compared = permission.compare(str(event.sender.user_id), target, str(event.group_id))
    has_permission = compared[0] >= 1 or event.sender.role == "owner"
    in_ops = compared[1] == 1
    if is_valid and has_permission and in_ops:
        # 分类讨论
        if constants.BotConstants.db_type in ["mysql", "sqlite"]:
            data = datautil.lookup("ops", f"userid_{target}")
            selected = [x for x in data if x['groupid'] == str(event.group_id)][0]
            datautil.delete("ops", f"recordid_{selected['recordid']}")
            permission.update_cache("ops")
            await deop.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(f" 已撤销 {target} 的本群机器人管理员权限")
            ]))
        else:
            data = datautil.lookup("ops", f"userid_{target}")[0]
            groups = data['groups']
            list(groups).remove(str(event.group_id))
            if len(groups) == 0:
                datautil.delete("ops", f"userid_{target}")
            else:
                modified_data = {
                    "groups": groups
                }
                datautil.modify("ops", f"userid_{target}", modified_data)
    elif not has_permission:
        await deop.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法撤销本群机器人管理员权限：宁踏马有权限吗？（恼）")
        ]))
    elif not in_ops:
        await deop.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法撤销本群机器人管理员权限：目标不是本群机器人管理员")
        ]))
    elif not is_valid:
        await deop.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法撤销本群机器人管理员权限：宁这是数字吗？（恼）")
        ]))
