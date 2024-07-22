import random
from math import floor

from arclet.alconna import Alconna, Arparma, Arg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_tasks import batch_expiration, batch_production
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·拿面包",
    description="从面包厂拿面包",
    usage=""
)

get_bread = on_alconna(
    Alconna("get_bread", Arg("amount", int, 1)),
    priority=10,
    use_cmd_start=True
)

bread_types = [
    chr(0x1f35e),
    chr(0x1f956),
    chr(0x1f950),
    chr(0x1f96f),
    chr(0x1f369)
]


# 消耗面包批次
def use_batch(group_id: str, deducted_amount: int):
    datautil = factory.DataUtilFactory.create_data_util()
    bread_batch = datautil.lookup("breadbatch", f"groupid_{group_id}")
    sorted_batch = sorted(bread_batch, key=lambda x: x['expiry'])
    cursor = 0
    while deducted_amount > 0 and cursor < len(sorted_batch):
        batch = sorted_batch[cursor]
        if deducted_amount >= batch["amount"]:
            deducted_amount -= batch["amount"]
            datautil.delete("breadbatch", f"batchid_{batch['batchid']}")
        else:
            batch["amount"] -= deducted_amount
            deducted_amount = 0
            datautil.modify("breadbatch", f"batchid_{batch['batchid']}", {"amount": batch["amount"]})
        cursor += 1


# 分配面包
def allocate_breads(amount: int):
    text = ""
    fields = [0 for _ in range(len(bread_types))]
    bread_sum = 0
    for i in range(len(fields) - 1):
        exponent = 0.5 - (i * (0.5 / len(bread_types)))
        fields[i] = random.randint(0,
                                   floor((amount - bread_sum) * (1 - exponent)))
        bread_sum += fields[i]
    fields[len(fields) - 1] = amount - bread_sum
    if amount <= 20:
        for i in range(len(bread_types)):
            text += bread_types[i] * fields[i]
    else:
        for i in range(len(bread_types)):
            text += f"\n{bread_types[i]} * {fields[i]}"
    return text


@get_bread.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    datautil = factory.DataUtilFactory.create_data_util()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        batch_expiration.execute(str(event.group_id))
        batch_production.execute(str(event.group_id))
        obj = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
        minimum_amount = len(bread_types) if "diverse" in obj["supply_mode"] else 1
        deducted_amount = 0 if "infinite" in obj["supply_mode"] else result.query("amount")
        bread_batch = datautil.lookup("breadbatch", f"groupid_{event.group_id}")
        at_least_minimum = result.query("amount") >= minimum_amount
        amounts = [x['amount'] for x in bread_batch]
        sufficient_breads = deducted_amount == 0 or sum(amounts) > deducted_amount
        if at_least_minimum and sufficient_breads:
            use_batch(str(event.group_id), deducted_amount)
            if "diverse" in obj["supply_mode"]:
                text = allocate_breads(result.query("amount"))
            else:
                text = bread_types[0] * result.query("amount") if result.query("amount") <= 20 \
                    else f"{bread_types[0]} * {result.query('amount')}"
            await get_bread.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(f" {text}")
            ]))
        elif not sufficient_breads:
            await get_bread.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 仓库里面包都不够你吃的，让我拿空气出来？臭啥比（恼）")
            ]))
        elif not at_least_minimum:
            await get_bread.finish(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(f" 这么点你让我怎么分？（恼）（至少需要 {minimum_amount} 个）")
            ]))
    else:
        await get_bread.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群，踏马连个面包厂都没有（恼）")
        ]))
