from textwrap import dedent

from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_tasks import batch_expiration, batch_production
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="面包厂·查询",
    description="查询面包厂信息",
    usage=""
)

query = on_alconna(
    Alconna("query"),
    priority=10,
    use_cmd_start=True
)


@query.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    factory_exists = datautil.is_here("breadfactory", f"groupid_{event.group_id}")
    if factory_exists:
        batch_expiration.execute(str(event.group_id))
        batch_production.execute(str(event.group_id))
        obj1 = datautil.lookup("breadfactory", f"groupid_{event.group_id}")[0]
        supply_modes = [
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
        production_modes = [
            "processed",
            "fresh"
        ]
        production_mode_names = [
            "加工面包生产模式",
            "新鲜面包生产模式"
        ]
        is_max_level = obj1["factory_level"] == 5
        bread_batch = datautil.lookup("breadbatch", f"groupid_{event.group_id}")
        material_batch = datautil.lookup("materialbatch", f"groupid_{event.group_id}")
        breads = sum([x['amount'] for x in bread_batch])
        flour = sum([x['amount'] for x in material_batch if x['type'] == "flour"])
        egg = sum([x['amount'] for x in material_batch if x['type'] == "egg"])
        yeast = sum([x['amount'] for x in material_batch if x['type'] == "yeast"])
        max_storage = 64 * pow(4, obj1["factory_level"]) * pow(2, obj1["storage_level"])
        cycle = 300 - 20 * (obj1["factory_level"] - 1) - 10 * obj1["speed_level"]
        output = pow(4, obj1["factory_level"]) * pow(2, obj1["output_level"])
        info = f"""\
        本群 ({event.group_id}) 面包厂信息如下：
        -----面包厂属性-----
        面包厂等级：{obj1["factory_level"]}{" / 5" if not is_max_level else "（满级）"}
        {f"库存升级次数：{obj1['storage_level']}" if is_max_level else ""}
        {f"生产速度升级次数：{obj1['storage_level']}" if is_max_level else ""}
        {f"产量升级次数：{obj1['storage_level']}" if is_max_level else ""}
        面包厂经验：{obj1["factory_exp"]} XP
        今日已获得经验：{obj1["exp_gained_today"]} / {300 * pow(2, (obj1["factory_level"] - 1))}
        供应模式：{supply_mode_names[supply_modes.index(obj1["supply_mode"])]}
        生产模式：{production_mode_names[production_modes.index(obj1["production_mode"])]}
        -----面包厂配置-----
        面包库存上限：{max_storage} 块
        生产周期：{cycle} 秒
        每周期最大产量：{output} 块
        -----批次保质期-----
        面粉保质期：{f"{obj1['flour_expiration']} 天" if obj1['flour_expiration'] != 0 else "永不过期"}
        鸡蛋保质期：{f"{obj1['egg_expiration']} 天" if obj1['egg_expiration'] != 0 else "永不过期"}
        酵母保质期：{f"{obj1['yeast_expiration']} 天" if obj1['yeast_expiration'] != 0 else "永不过期"}
        面包保质期：{f"{obj1['bread_expiration']} 天" if obj1['bread_expiration'] != 0 else "永不过期"}
        -----物品库存-----
        现有原材料：{flour} 份面粉、{egg} 份鸡蛋、{yeast} 份酵母
        现有面包：{breads} / {max_storage} 块
        """
        lines = info.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        info = '\n'.join(non_empty_lines)
        await query.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text("\n"),
            MessageSegment.text(dedent(info))
        ]))
    else:
        await query.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 这b群，踏马连个面包厂都没有（恼）")
        ]))
