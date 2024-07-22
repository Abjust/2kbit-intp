from math import ceil

from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·升级仓库",
    description="升级面包厂的仓库等级",
    usage=""
)

upgrade_storage = on_alconna(
    Alconna("upgrade_storage"),
    priority=10,
    use_cmd_start=True
)


@upgrade_storage.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        obj = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
        formula = ceil(9600 * pow(1.14, obj["storage_level"] - 1))
        is_maxed = obj["factory_level"] == 5
        storage_not_maxed = obj["storage_level"] < 16
        sufficient_exp = obj["factory_exp"] >= formula
        if is_maxed and storage_not_maxed and sufficient_exp:
            modified_data = {
                "storage_level": obj["storage_level"] + 1,
                "factory_exp": obj["factory_exp"] - formula
            }
            datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
            await upgrade_storage.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(f" 已将面包厂仓库等级升级到 {obj['storage_level'] + 1} 级")
            ]))
        elif not sufficient_exp:
            await upgrade_storage.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(f" byd，升级面包厂仓库等级需要 {formula} 点经验，"
                                    f"但是本群面包厂还差 {formula - obj['factory_exp']} 点经验，你升牛魔（恼）")
            ]))
        elif not storage_not_maxed:
            await upgrade_storage.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 这b群，面包厂仓库踏马已经满级了（恼）")
            ]))
        elif not is_maxed:
            await upgrade_storage.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 这b群，面包厂踏马还没满级（恼）")
            ]))
    else:
        await upgrade_storage.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群，踏马连个面包厂都没有（恼）")
        ]))
