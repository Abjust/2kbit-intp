from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

from codeintp import initialization
from codeintp.bot_utils import permission, turned_off

__plugin_meta__ = PluginMetadata(
    name="群消息事件代理",
    description="如果来源群或者qq被屏蔽，则阻断消息事件，否则转发给其他模块",
    usage=""
)

forward_event = on_message(rule=is_type(GroupMessageEvent), priority=2, block=False)


@forward_event.handle()
async def handle_function(matcher: Matcher, event: GroupMessageEvent):
    initialization.execute()
    if permission.is_group_ignored(str(event.sender.user_id), str(event.group_id)) \
            or str(event.group_id) in turned_off.turned_off:
        forward_event.stop_propagation(matcher)
