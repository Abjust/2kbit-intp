from textwrap import dedent

from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="心理健康科普",
    description="提供各类精神心理量表和性格测试",
    usage=""
)

from nonebot.rule import is_type

mental_health = on_message(is_type(GroupMessageEvent), priority=100)

scales = [
    "MBTI",
    "艾森克",
    "大五",
    "九型",
    "黑暗人格",
    "道德九宫格",
    "SCL90",
    "SDS",
    "SAS"
]
links = [
    "https://www.jungus.cn/zh-hans/test/",
    "7-15：https://www.psy525.cn/ceshi/84336.html\r\n16+：https://www.psy525.cn/ceshi/84335.html",
    "https://www.apesk.com/bigfive_step2/",
    "https://www.ifreesite.com/enneagram/enneagram.htm",
    "https://qst.darkfactor.org",
    "https://unnamed42.github.io/2016-06-30-%E5%AE%98%E6%96%B9%E7%89%88DnD%E9%98%B5%E8%90%A5%E6%B5%8B%E8%AF%95.html",
    "http://www.ntneuro.org/scale/scl90.asp",
    "https://www.zxgj.cn/g/yiyuzheng",
    "https://www.zxgj.cn/g/jiaolv"
]


@mental_health.handle()
async def handle_function(event: GroupMessageEvent):
    if event.message.extract_plain_text() == "量表测试大全":
        await mental_health.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text("\n"),
            MessageSegment.text(dedent("""\
                量表测试大全
                人格/性格测试：
                MBTI|艾森克
                大五|九型
                黑暗人格|道德九宫格
                精神心理量表：
                SCL90（综合）|SDS（抑郁）
                SAS（焦虑）
                （精神心理量表结果仅供参考，如出现相关症状，还请尽快前往当地医院就诊）
                """))
        ]))
    else:
        for scale in scales:
            if str.upper(event.message.extract_plain_text()) == scale:
                await mental_health.finish(Message([
                    MessageSegment.reply(event.message_id),
                    MessageSegment.at(event.sender.user_id),
                    MessageSegment.text("\n"),
                    MessageSegment.text(links[scales.index(scale)])
                ]))
                break
