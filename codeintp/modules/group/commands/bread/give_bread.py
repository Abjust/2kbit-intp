import datetime
import random

from arclet.alconna import Alconna, Arg, Arparma
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_tasks import batch_expiration, batch_production
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·给面包",
    description="给面包厂一些面包",
    usage=""
)

give_bread = on_alconna(
    Alconna("give_bread", Arg("amount", int, 1)),
    priority=10,
    use_cmd_start=True
)


@give_bread.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        time_now = datetime.datetime.now().timestamp()
        batch_expiration.execute(str(event.group_id))
        batch_production.execute(str(event.group_id))
        obj = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
        normal_supply = obj["supply_mode"] == "normal"
        at_least_one = result.query("amount") > 0
        max_storage = 64 * pow(4, obj["factory_level"]) * pow(2, obj["storage_level"])
        bread_batch = datautil.lookup("breadbatch", f"groupid_{event.group_id}")
        amounts = [x['amount'] for x in bread_batch]
        not_full = sum(amounts) + result.query("amount") <= max_storage
        if normal_supply and at_least_one and not_full:
            r = random.randint(100000, 999999)
            if datautil.is_here("breadbatch", f"batchid_{r}"):
                while datautil.is_here("breadbatch", f"batchid_{r}"):
                    r = random.randint(100000, 999999)
            obj1 = {
                "batchid": r,
                "groupid": event.group_id,
                "amount": result.query("amount"),
                "expiry": time_now + 86400
            }
            datautil.add("breadbatch", obj1)
            await give_bread.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(f" 现在库存有 {obj['breads'] + result.query('amount')} 块面包辣！")
            ]))
        elif not not_full:
            await give_bread.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 库存满了就不要塞面包进来了，老蝉（恼）")
            ]))
        elif not at_least_one:
            await give_bread.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 这你让我怎么理解？（恼）")
            ]))
        elif not normal_supply:
            await give_bread.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" byd能不能把供应模式改改？（恼）")
            ]))
    else:
        await give_bread.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群，踏马连个面包厂都没有（恼）")
        ]))
