import datetime
from math import log10, trunc, ceil
from textwrap import dedent

import opencc
import pytz
from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

from codeintp.bot_tasks import woodenfish_tasks
from codeintp.bot_utils.datautil import factory

__plugin_meta__ = PluginMetadata(
    name="木鱼·我的木鱼",
    description="显示木鱼信息",
    usage=""
)

info = on_alconna(
    Alconna(opencc.OpenCC("t2s.json").convert("我的木鱼")),
    priority=10
)


# 转换功德
def conversion(obj):
    datautil = factory.DataUtilFactory.create_data_util()
    if log10(obj["gongde"]) >= 6 and obj["e"] <= 200:
        modified_data = {
            "e": log10(pow(10, obj["e"]) + obj["gongde"]),
            "gongde": 0
        }
        datautil.modify("woodenfish", f"playerid_{obj['playerid']}", modified_data)
    if log10(obj["e"]) >= 2 and obj["ee"] <= 200:
        modified_data = {
            "ee": log10(pow(10, obj["ee"]) + obj["e"]),
            "e": 0
        }
        datautil.modify("woodenfish", f"playerid_{obj['playerid']}", modified_data)


# 生成数学表达式
def get_expression(obj):
    expression = ""
    expression_low = ""
    if obj["ee"] >= 1:
        expression = f"(10^10^{trunc(10000 * obj['ee']) / 10000})"
        expression_low = f"(10^{trunc(10000 * obj['e']) / 10000})"
        gongde = f"ee{trunc(10000 * obj['ee']) / 10000}（{expression}）"
        gongde_low = f"\ne (log10)：{trunc(10000 * obj['e']) / 10000}（{expression_low}）\n原始功德：{obj['gongde']}"
    elif obj["e"] >= 1:
        expression = f"(10^{trunc(10000 * obj['e']) / 10000})"
        gongde = f"ee{trunc(10000 * obj['e']) / 10000}（{expression}）"
        gongde_low = f"\n原始功德：{obj['gongde']}"
    else:
        gongde = f"{obj['gongde']}"
        gongde_low = "无"
    return gongde, expression, gongde_low, expression_low


# 自动涅槃
def auto_nirvana(obj):
    datautil = factory.DataUtilFactory.create_data_util()
    if obj["ee"] >= 300:
        if obj["nirvana"] + 0.02 <= 5:
            modified_data = {
                "nirvana": trunc((obj["nirvana"] + 0.2) * 100) / 100
            }
            datautil.modify("woodenfish", f"playerid_{obj['playerid']}", modified_data)
        else:
            modified_data = {
                "nirvana": 5
            }
            datautil.modify("woodenfish", f"playerid_{obj['playerid']}", modified_data)
        modified_data = {
            "level": 1,
            "gongde": 0,
            "e": 0,
            "ee": 0
        }
        datautil.modify("woodenfish", f"playerid_{obj['playerid']}", modified_data)


@info.handle()
async def handle_function(event: GroupMessageEvent):
    datautil = factory.DataUtilFactory.create_data_util()
    status = ""
    tips = ""
    time_now = datetime.datetime.now().timestamp()
    if datautil.is_here("woodenfish", f"playerid_{event.sender.user_id}"):
        woodenfish_tasks.get_exp(event.sender.user_id)
        obj = datautil.lookup("woodenfish", f"playerid_{event.sender.user_id}")
        if obj["info_ctrl"] < time_now:
            if obj["ban"] == 0:
                status = "正常"
                tips = "【敲电子木鱼，见机甲佛祖，取赛博真经】"
                conversion(obj)
            elif obj["ban"] == 1:
                status = "永久封禁中"
                tips = "【我说那个佛祖啊，我刚刚在刷功德的时候，你有在偷看罢？】"
            elif obj["ban"] == 2 and time_now < obj["dt"]:
                time = (pytz.utc.localize(datetime.datetime.fromtimestamp(obj["dt"]))
                        .astimezone(pytz.timezone("Asia/Shanghai")))
                status = f"暂时封禁中（直至：{time}）"
                tips = "【待封禁结束后，可发送“我的木鱼”解封】"
            elif obj["ban"] == 2:
                status = "正常"
                tips = "【敲电子木鱼，见机甲佛祖，取赛博真经】"
                modified_data = {
                    "ban": 0,
                    "time": time_now
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
            if time_now - obj["info_time"] <= 10:
                modified_data = {
                    "info_count": obj["info_count"] + 1
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
            else:
                modified_data = {
                    "info_count": 1,
                    "info_time": time_now
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
            auto_nirvana(obj)
            await info.send(Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.at(event.user_id),
                MessageSegment.text(" 宁踏马功德太多辣（恼）（已自动涅槃重生，涅槃值+0.2）")
            ]))
            obj = datautil.lookup("woodenfish", f"playerid_{event.sender.user_id}")
            expressions = get_expression(obj)
            if time_now - obj["info_time"] <= 10 and obj["info_count"] > 5:
                modified_data = {
                    "info_ctrl": time_now + 180,
                    "info_count": 0
                }
                datautil.modify("woodenfish", f"playerid_{event.sender.user_id}", modified_data)
                await info.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(" 宁踏马3分钟之内也别想用我的木鱼辣（恼）")
                ]))
            else:
                await info.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.user_id),
                    MessageSegment.text(dedent(f"""
                        赛博账号：{event.sender.user_id}
                        账号状态：{status}
                        木鱼等级：{obj["level"]}
                        涅槃值：{obj["nirvana"]}
                        当前速度：{ceil(60 * pow(0.978, obj["level"] - 1))} 秒/周期
                        当前功德：{expressions[0]} {expressions[1]}
                        低级功德储备：{expressions[2]} {expressions[3]}
                        {tips}
                        """).strip())
                ]))
    else:
        await info.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.user_id),
            MessageSegment.text(" 宁踏马害没注册？快发送“给我木鱼”注册罢！")
        ]))
