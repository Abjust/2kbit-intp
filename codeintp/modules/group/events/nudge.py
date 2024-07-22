import random

import requests
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, Message, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.rule import is_type

__plugin_meta__ = PluginMetadata(
    name="戳机器人",
    description="敢不敢和我比划比划？",
    usage=""
)

import constants
from codeintp.bot_utils.logger import bot_logger

words = [
    "cnmd",
    "你更是歌姬吧嗷",
    "你个狗比玩意",
    "你是不是被抛上去3次，却只被接住2次？",
    "你真是小母牛坐灯泡，牛逼一闪又一闪",
    "小嘴像抹了开塞露一样",
    "小东西长得真随机",
    "我只想骂人，但不想骂你",
    "但凡你有点用，也不至于一点用处都没有",
    "你还真把自己当个人看了，你也配啊",
    "那么丑的脸，就可以看出你是金针菇",
    "阁下长得真是天生励志",
    "装逼对你来说就像一日三餐的事",
    "我怎么敢碰你呢，我怕我买洗手液买穷自己",
    "狗咬了你，你还能咬回狗吗",
    "你是独一无二的，至少全人类都不希望再有第二个",
    "你的智商和喜马拉雅山的氧气一样，稀薄",
    "别人的脸是七分天注定，三分靠打扮，你的脸是一分天注定，九分靠滤镜",
    "偶尔也要活得强硬一点，软得像滩烂泥一样有什么意思",
    "任何人工智能都敌不过阁下这款天然呆",
    "我骂你是为了你好，你应该从中学到些什么，比如说自知之明",
    "你要好好做自己，反正别的你也做不好",
    "如果国家把长相分等级的话，你的长相，都可以吃低保了",
    "你没权利看不惯我的生活方式，但你有权抠瞎自己的双眼",
    "如果你觉得我哪里不对，请一定要告诉我，反正我也不会改，你别憋出病来",
    "你（  ）什么时候（  ）啊",
    "四吗玩意，说我是歌姬吧，你怎么不撒泡尿照照镜子看看你自己，狗比玩意",
    "握草泥马呀—\r\n我操尼玛啊啊啊啊—\r\n我—操—你—妈—\r\n听到没，我—操—你—妈—"
]

nudge = on_notice(is_type(PokeNotifyEvent))


@nudge.handle()
async def handle_function(event: PokeNotifyEvent):
    if event.group_id is not None and event.target_id == constants.BotConstants.bot_qq:
        fetch = random.randrange(2) == 1
        index = random.randrange(len(words))
        if fetch:
            apis = [
                "https://api.qhsou.com/api/zuan.php",
                "http://api.qemao.com/api/yulu/?type=2"
            ]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
                'Content-Type': 'application/json'
            }
            api_index = random.randrange(len(apis))
            try:
                response = requests.get(apis[api_index], headers)
                if response.ok and response.content != "":
                    word = response.content.strip().decode("utf-8")
                else:
                    word = words[index]
            except Exception as ex:
                word = words[index]
                bot_logger.error(ex)
        else:
            word = words[index]
        await nudge.finish(Message([
            MessageSegment.at(event.user_id),
            MessageSegment.text(" "),
            MessageSegment.text(word)
        ]))
