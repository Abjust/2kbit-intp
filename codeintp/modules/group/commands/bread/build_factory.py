import datetime

from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·建造工厂",
    description="给群造个面包厂",
    usage=""
)

build_factory = on_alconna(
    Alconna("build_factory"),
    priority=10,
    use_cmd_start=True
)


@build_factory.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    columns1 = [
        ("groupid", "varchar(16)", True),
        ("factory_level", "int", False),
        ("storage_level", "int", False),
        ("speed_level", "int", False),
        ("output_level", "int", False),
        ("supply_mode", "varchar(16)", False),
        ("production_mode", "varchar(16)", False),
        ("factory_exp", "int", False),
        ("exp_gained_today", "int", False),
        ("last_expfull", "bigint", False),
        ("last_expgain", "bigint", False),
        ("last_produce", "bigint", False),
        ("expiration", "int", False),
    ]
    columns2 = [
        ("batchid", "int", True),
        ("groupid", "varchar(16)", False),
        ("type", "varchar(16)", False),
        ("amount", "int", False),
        ("expiry", "bigint", False)
    ]
    columns3 = [
        ("batchid", "int", True),
        ("groupid", "varchar(16)", False),
        ("amount", "int", False),
        ("expiry", "bigint", False)
    ]
    datautil.initialize("breadfactory", columns1)
    datautil.initialize("materialbatch", columns2)
    datautil.initialize("breadbatch", columns3)
    if not factory_exists:
        obj1 = {
            "_key.groupid": f"{event.group_id}",
            "factory_level": 1,
            "storage_level": 0,
            "speed_level": 0,
            "output_level": 0,
            "supply_mode": "normal",
            "production_mode": "fresh",
            "factory_exp": 0,
            "exp_gained_today": 0,
            "last_expfull": 946656000,
            "last_expgain": 946656000,
            "last_produce": int(datetime.datetime.now().timestamp()),
            "flour_expiration": 90,
            "egg_expiration": 45,
            "yeast_expiration": 180,
            "bread_expiration": 3
        }
        datautil.add("breadfactory", obj1)
        await build_factory.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 成功为本群建造面包厂！")
        ]))
    else:
        await build_factory.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群踏马已经有面包厂辣（恼）")
        ]))
