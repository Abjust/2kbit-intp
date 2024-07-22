import datetime
import json

import requests
from arclet.alconna import Alconna, Arparma, Arg
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="DNS查询",
    description="查询所有DNS记录",
    usage=""
)

dns_lookup = on_alconna(
    Alconna("dns_lookup", Arg("domain", str), Arg("flush", bool, False)),
    priority=10,
    use_cmd_start=True
)


@dns_lookup.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    time_now = datetime.datetime.now().timestamp()
    time_midnight = time_now - (time_now + 8 * 3600) % 86400
    columns = [
        ("domain", "varchar(255)", True),
        ("records", "text", False),
        ("cache_ends", "bigint", False)
    ]
    datautil.initialize("dns_cache", columns)

    def get_record():
        url = "https://api.siterelic.com/dnsrecord"
        headers = {
            'x-api-key': 'ffe4de0c-b2e3-4591-88ab-afdd17d00b52',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "url": result.query[str]("domain")
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    if not datautil.is_here("dns_cache", f"domain_{result.query[str]('domain')}"):
        records = get_record()
        if records.status_code == 200:
            obj = {
                "domain": result.query[str]('domain'),
                "records": records.text,
                "cache_ends": time_midnight + 31 * 86400
            }
            datautil.add("dns_cache", obj)
            await dns_lookup.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text("\n"),
                MessageSegment.text(records.text)
            ]))
        else:
            await dns_lookup.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text("\n"),
                MessageSegment.text(f"执行查询时出错！错误代码：{records.status_code}")
            ]))
    else:
        obj1 = datautil.lookup("dns_cache", f"domain_{result.query[str]('domain')}")[0]
        if time_now >= obj1["cache_ends"] or result.query("flush") is True:
            await dns_lookup.send(Message([
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(
                    " 注意：已在缓存表找到此域名，但是缓存已经过期，或者用户要求刷新缓存，正在尝试拉取新的记录！")
            ]))
            records = get_record()
            if records.status_code == 200:
                modified_data = {
                    "records": records.text,
                    "cache_ends": time_midnight + 31 * 86400
                }
                datautil.modify("dns_cache", f"domain_{result.query[str]('domain')}", modified_data)
                await dns_lookup.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text("\n"),
                    MessageSegment.text(records.text)
                ]))
            else:
                await dns_lookup.send(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text("\n"),
                    MessageSegment.text(
                        f"执行查询时出错！错误代码：{records.status_code}（这意味着将从过期的缓存拉取结果）")
                ]))
                await dns_lookup.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text("\n"),
                    MessageSegment.text(obj1["records"])
                ]))

        else:
            await dns_lookup.send(Message([
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text(" 注意：已在缓存表找到此域名，此次查询已从缓存表拉取！")
            ]))
            await dns_lookup.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.sender.user_id),
                MessageSegment.text("\n"),
                MessageSegment.text(obj1["records"])
            ]))
