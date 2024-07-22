from operator import itemgetter

import opencc
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·封禁榜",
    description="这有比的必要吗（恼）",
    usage=""
)

ban_leaderboard = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("封禁榜")),
    priority=10
)


@ban_leaderboard.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("woodenfish"):
        results = sorted(datautil.lookup("woodenfish"),
                         key=itemgetter("total_ban"), reverse=True)
        listed = []
        limit = 10
        message_chain = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text("\n封禁榜\n赛博账号 --- 累计封禁次数")
        ])
        for item in results:
            if len(listed) >= limit:
                break
            if item["total_ban"] >= 1:
                message_chain1 = Message([
                    MessageSegment.text(f"\n{item['playerid']} --- {item['total_ban']}")
                ])
                message_chain += message_chain1
        await ban_leaderboard.finish(message_chain)
    else:
        await ban_leaderboard.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 还没有人注册赛博账号！")
        ]))
