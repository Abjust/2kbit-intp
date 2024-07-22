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
    name="群管·本群解黑",
    description="将某个人从本群的黑名单中移除",
    usage=""
)

unblock = on_alconna(
    Alconna("unblock", Arg("target", Any)),
    priority=10,
    use_cmd_start=True
)


@unblock.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    target = str(identify(result.query("target")).strip())
    is_valid = target.isdigit()
    compared = permission.compare(str(event.sender.user_id), target, str(event.group_id))
    has_permission = compared[0] >= 1
    in_blocklist = permission.is_group_blocked(identify(result.query("target")), str(event.group_id))
    if is_valid and has_permission and in_blocklist:
        # 分类讨论
        if constants.BotConstants.db_type in ["mysql", "sqlite"]:
            data = datautil.lookup("blocklist", f"userid_{target}")
            selected = [x for x in data if x['groupid'] == str(event.group_id)][0]
            datautil.delete("blocklist", f"recordid_{selected['recordid']}")
            permission.update_cache("blocklist")
            await unblock.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(f" 已将 {target} 移出本群黑名单")
            ]))
        else:
            data = datautil.lookup("blocklist", f"userid_{target}")[0]
            groups = data['groups']
            list(groups).remove(str(event.group_id))
            if len(groups) == 0:
                datautil.delete("blocklist", f"userid_{target}")
            else:
                modified_data = {
                    "groups": groups
                }
                datautil.modify("blocklist", f"userid_{target}", modified_data)
    elif not has_permission:
        await unblock.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法解黑：宁踏马有权限吗？（恼）")
        ]))
    elif not in_blocklist:
        await unblock.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法解黑：目标不在本群黑名单")
        ]))
    elif not is_valid:
        await unblock.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 无法解黑：宁这是数字吗？（恼）")
        ]))
