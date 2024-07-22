from math import trunc
from operator import itemgetter

import opencc
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·功德榜",
    description="功德无量",
    usage=""
)

leaderboard = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("功德榜")),
    priority=10
)


@leaderboard.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    if datautil.is_here("woodenfish"):
        results = sorted(datautil.lookup("woodenfish"),
                         key=itemgetter("ee"), reverse=True)
        results_ee = [(x['userid'], f"ee{trunc(x['ee'] * 10000) / 10000}") for x in results if round(x['ee'], 4) >= 1]
        results = sorted(datautil.lookup("woodenfish"),
                         key=itemgetter("e"), reverse=True)
        results_e = [(x['userid'], f"e{trunc(x['e'] * 10000) / 10000}") for x in results if round(x['e'], 4) >= 1]
        results = sorted(datautil.lookup("woodenfish"),
                         key=itemgetter("gongde"), reverse=True)
        results_gongde = [(x['userid'], f"{x['gongde']}") for x in results if x['gongde'] >= 1]
        results = results_ee + results_e + results_gongde
        listed = []
        limit = 10
        message_chain = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text("\n功德榜\n赛博账号 --- 功德")
        ])
        for item in results:
            if len(listed) >= limit:
                break
            listed.append(item[0])
            message_chain1 = Message([
                MessageSegment.text(f"\n{item[0]} --- {item[1]}")
            ])
            message_chain += message_chain1
        await leaderboard.finish(message_chain)
    else:
        await leaderboard.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 还没有人注册赛博账号！")
        ]))
