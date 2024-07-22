from arclet.alconna import Subcommand, Arg, Alconna, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·设置过期时间",
    description="设置一批原材料或者面包的过期时间",
    usage=""
)

set_expiry = on_alconna(
    Alconna("set_expiry",
            Subcommand(
                "flour", Arg("expiration", int, 90)
            ),
            Subcommand(
                "egg", Arg("expiration", int, 45)
            ),
            Subcommand(
                "yeast", Arg("expiration", int, 180)
            ),
            Subcommand(
                "bread", Arg("expiration", int, 3)
            )),
    priority=10,
    use_cmd_start=True
)


@set_expiry.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    obj = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
    minimum_expiration = 0
    maximum_expiration = 0
    name = ""
    subcommand = list(result.subcommands.keys())[0]
    if result.find("flour"):
        minimum_expiration = 90
        maximum_expiration = 360
        name = "面粉"
    elif result.find("egg"):
        minimum_expiration = 45
        maximum_expiration = 60
        name = "鸡蛋"
    elif result.find("yeast"):
        minimum_expiration = 180
        maximum_expiration = 360
        name = "酵母"
    elif result.find("bread") and obj["production_mode"] == "processed":
        minimum_expiration = 90
        maximum_expiration = 120
        name = "加工面包"
    elif result.find("bread"):
        minimum_expiration = 1
        maximum_expiration = 3
        name = "新鲜面包"
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        expiration_not_same = result.query("expiration") != obj[f"{subcommand}_expiration"]
        expiration_is_valid = (result.query("expiration") == 0
                               or (minimum_expiration <= result.query("expiration") <= maximum_expiration))
        bread_expiration = 90 if obj["production_mode"] == "processed" else 3
        if expiration_not_same and expiration_is_valid:
            datautil.delete("materialbatch", f"groupid_{event.group_id}")
            datautil.delete("breadbatch", f"groupid_{event.group_id}")
            if result.query("expiration") == 0:
                modified_data = {
                    "flour_expiration": 0,
                    "egg_expiration": 0,
                    "yeast_expiration": 0,
                    "bread_expiration": 0
                }
                datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
                datautil.delete("materialbatch", f"groupid_{event.group_id}")
                datautil.delete("breadbatch", f"groupid_{event.group_id}")
                await set_expiry.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(f" 已将{name}的保质期设置为：永不过期（连锁反应已触发，所有批次库存已自动清空）")
                ]))
            elif result.query("expiration") != 0 and obj[f"{subcommand}_expiration"] == 0:
                modified_data = {
                    "flour_expiration": 90,
                    "egg_expiration": 45,
                    "yeast_expiration": 180,
                    "bread_expiration": bread_expiration,
                    f"{subcommand}_expiration": result.query("expiration")
                }
                datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
                await set_expiry.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(
                        f" 已将{name}的保质期设置为：{result.query('expiration')} 天（连锁反应已触发，且所有批次库存已自动清空）")
                ]))
            else:
                modified_data = {
                    f"{subcommand}_expiration": result.query("expiration")
                }
                datautil.modify("breadfactory", f"groupid_{event.group_id}", modified_data)
                await set_expiry.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(
                        f" 已将{name}的保质期设置为：{result.query('expiration')} 天（所有批次库存已自动清空）")
                ]))
        elif not expiration_is_valid:
            await set_expiry.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(
                    f" {name}的保质期只能介于{minimum_expiration}~{maximum_expiration}天，也可设置为0（永不过期）")
            ]))
        elif not expiration_not_same:
            await set_expiry.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(
                    f" {name}新设置的保质期不能和原来一样")
            ]))
    else:
        await set_expiry.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群，踏马连个面包厂都没有（恼）")
        ]))
