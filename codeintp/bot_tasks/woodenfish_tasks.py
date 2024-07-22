import datetime
import math
from math import ceil, floor, log10

from codeintp.bot_utils.datautil import factory


def get_exp(player_id):
    datautil = factory.DataUtilFactory.create_data_util()
    time_now = datetime.datetime.now().timestamp()
    obj = datautil.lookup("woodenfish", f"playerid_{player_id}")
    if obj["ban"] != 0:
        return
    cycle_speed = ceil(60 * pow(0.978, obj["level"] - 1))
    elapsed_time = time_now - obj["time"]
    if elapsed_time < cycle_speed:
        return
    e = obj["e"]
    gongde = 0
    cycles = min(12 + obj["level"] - 1, floor(elapsed_time / cycle_speed))
    actual_cycles = min(cycles, 120)
    for _ in range(actual_cycles):
        if e >= 200:
            break
        e = log10((pow(10, e) + obj["gongde"])) * pow(math.e, obj["nirvana"]) + obj["level"]
        gongde = round(pow(10, e - floor(e)))
    new_e = e if e >= 6 else 0
    new_gongde = gongde if e >= 6 else round(pow(10, e) + gongde)
    new_time = time_now - (elapsed_time % cycle_speed)
    modified_data = {
        "e": new_e,
        "gongde": new_gongde,
        "time": new_time
    }
    datautil.modify("woodenfish", f"playerid_{player_id}", modified_data)
