import random

from arclet.alconna import Alconna
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="显示版本",
    description="显示2kbit Code: INTP的当前版本",
    usage=""
)

version = on_alconna(
    Alconna("版本"),
    priority=10
)

splashes = [
    "也试试HanBot罢！Also try HanBot!",
    "誓死捍卫微软苏维埃！",
    "要把反革命分子的恶臭思想，扫进历史的垃圾堆！",
    "PHP是世界上最好的编程语言（雾）",
    "社会主义好，社会主义好~",
    "Minecraft很好玩，但也可以试试Terraria！",
    "So Nvidia, f**k you!",
    "战无不胜的马克思列宁主义万岁！",
    "Bug是杀不完的，你杀死了一个Bug，就会有千千万万个Bug站起来！",
    "跟张浩扬博士一起来学Jvav罢！",
    "哼哼哼，啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊",
    "你知道吗？其实你什么都不知道！",
    "Tips:这是一条烫...烫..烫知识（）",
    "你知道成功的秘诀吗？我告诉你成功的秘诀就是：我操你妈的大臭逼",
    "有时候ctmd不一定是骂人 可能是传统美德",
    "python不一定是编程语言 也可能是屁眼通红",
    "这条标语虽然没有用，但是是有用的，因为他被加上了标语",
    "使用Python编写！"
]


@version.handle()
async def handle_function(event: GroupMessageEvent):
    r = random.randrange(0, len(splashes))
    await version.finish(Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.at(event.sender.user_id),
        MessageSegment.text("\n"),
        MessageSegment.text("机器人版本：2kbit Code: INTP 1.0.0-beta4\n"
                            "上次更新日期：2024/7/23\n"
                            "更新内容：又修复了一些奇怪的bug\n"
                            "---------\n"
                            f"{splashes[r]}")
    ]))
