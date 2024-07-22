from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·升级工厂",
    description="升级面包厂的等级",
    usage=""
)

upgrade_factory = on_alconna(
    Alconna("upgrade_factory"),
    priority=10,
    use_cmd_start=True
)


@upgrade_factory.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        obj = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
        formula = 900 * pow(2, obj["factory_level"] - 1)
        not_maxed = obj["factory_level"] < 5
        sufficient_exp = obj["factory_exp"] >= formula
        if not_maxed and sufficient_exp:
            modified_data = {
                "factory_level": obj["factory_level"] + 1,
                "factory_exp": obj["factory_exp"] - formula
            }
            datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
            await upgrade_factory.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(f" 已将面包厂等级升级到 {obj['factory_level'] + 1} 级")
            ]))
        elif not sufficient_exp:
            await upgrade_factory.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(
                    f" byd，升级面包厂等级需要 {formula} 点经验，"
                    f"但是本群面包厂还差 {formula - obj['factory_exp']} 点经验，你升牛魔（恼）")
            ]))
        elif not not_maxed:
            await upgrade_factory.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 这b群，面包厂踏马已经满级了（恼）")
            ]))
    else:
        await upgrade_factory.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群，踏马连个面包厂都没有（恼）")
        ]))
