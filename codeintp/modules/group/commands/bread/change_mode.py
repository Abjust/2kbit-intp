from arclet.alconna import Alconna, Subcommand, Arparma, Arg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·更改模式",
    description="更改面包厂的生产或者供应模式",
    usage=""
)

change_mode = on_alconna(
    Alconna("change_mode",
            Subcommand(
                "production",
                Arg("mode", str),
            ),
            Subcommand(
                "supply",
                Arg("mode", str),
            )),
    priority=10,
    use_cmd_start=True
)

accepted_supply_modes = [
    "infinite_diverse",
    "infinite",
    "diverse",
    "normal"
]
supply_mode_names = [
    "多样化无限供应模式",
    "单一化无限供应模式",
    "多样化供应模式",
    "单一化供应模式"
]
accepted_production_modes = [
    "processed",
    "fresh"
]
production_mode_names = [
    "加工面包生产模式",
    "新鲜面包生产模式"
]


@change_mode.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        mode = result.query("mode")
        if result.find("production") and result.query("mode") in accepted_production_modes:
            modified_data = {
                "production_mode": result.query("mode"),
                "bread_expiration": 3 if result.query("mode") == "fresh" else 90
            }
            datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
            await change_mode.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(
                    f" 已更改生产模式！现在的生产模式为：{production_mode_names[accepted_production_modes.index(mode)]}")
            ]))
        elif result.find("supply") and result.query("mode") in accepted_supply_modes:
            modified_data = {
                "supply_mode": result.query("mode")
            }
            datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
            datautil.delete("breadbatch", f"groupid_{event.group_id}")
            await change_mode.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(
                    f" 已更改供应模式！现在的供应模式为：{supply_mode_names[accepted_supply_modes.index(mode)]}\n"
                    f"（面包批次已清空）")
            ]))
        elif result.find("production") or result.find("supply"):
            await change_mode.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 模式写错了，改牛魔（恼）")
            ]))
    else:
        await change_mode.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群，踏马连个面包厂都没有（恼）")
        ]))
