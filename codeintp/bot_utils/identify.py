# 识别at
from nonebot.adapters.onebot.v11 import MessageSegment


def identify(raw_data):
    if isinstance(raw_data, MessageSegment):
        return raw_data.data["qq"]
    else:
        return raw_data
