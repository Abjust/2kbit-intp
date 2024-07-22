from operator import itemgetter

import opencc
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·涅槃榜",
    description="功德更上一层楼",
    usage=""
)

nirvana_leaderboard = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("涅槃榜")),
    priority=10
)


@nirvana_leaderboard.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("woodenfish", ""):
        results = sorted(datautil.lookup("woodenfish", ""),
                         key=itemgetter("nirvana"), reverse=True)
        listed = []
        limit = 10
        message_chain = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text("\n涅槃榜\n赛博账号 --- 涅槃值")
        ])
        for item in results:
            if len(listed) >= limit:
                break
            if item["nirvana"] > 1:
                message_chain1 = Message([
                    MessageSegment.text(f"\n{item['playerid']} --- {item['nirvana']}")
                ])
                message_chain += message_chain1
        await nirvana_leaderboard.finish(message_chain)
    else:
        await nirvana_leaderboard.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 还没有人注册赛博账号！")
        ]))
