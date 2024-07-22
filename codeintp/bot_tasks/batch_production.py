import datetime
import random
from math import floor

from codeintp.bot_utils.datautil import factory


class BatchProcessor:
    def __init__(self, datautil):
        self.datautil = datautil

    # 生成批次编号
    def _generate_batch_id(self, batch_table: str) -> int:
        r = random.randint(100000, 999999)
        while self.datautil.is_here(batch_table, f"batchid_{r}"):
            r = random.randint(100000, 999999)
        return r

    # 加入到批次
    def _add_to_batch(self, batch_type: str, batch_id: int, group_id: str, amount: int, expiration: int):
        time_now = datetime.datetime.now().timestamp()
        obj = {
            "_key.batchid": batch_id,
            "groupid": group_id,
            "amount": amount,
            "expiry": time_now + expiration * 86400
        }
        if batch_type != "breadbatch":
            obj["type"] = batch_type
        self.datautil.add(batch_type, obj)

    # 获取批次
    @staticmethod
    def _get_batch(original_batch, batch_type: str):
        batch = [x for x in original_batch if x["type"] == batch_type]
        return sorted(batch, key=lambda x: x["expiry"])

    # 使用材料批次
    def _use_batch(self, batch_type: str, original_batch: list, deducted_amount: int):
        # 筛选出指定类型的材料
        selected_batch = [batch for batch in original_batch if batch['type'] == batch_type]
        # 按照过期时间从早到晚排序
        sorted_batch = sorted(selected_batch, key=lambda x: x['expiry'])
        cursor = 0
        while deducted_amount > 0 and cursor < len(sorted_batch):
            batch = sorted_batch[cursor]
            if deducted_amount >= batch["amount"]:
                deducted_amount -= batch["amount"]
                self.datautil.delete("materialbatch", f"batchid_{batch['batchid']}")
            else:
                batch["amount"] -= deducted_amount
                deducted_amount = 0
                self.datautil.modify("materialbatch", f"batchid_{batch['batchid']}", {"amount": batch["amount"]})
            cursor += 1

    # 生产材料
    def produce_material(self, obj: dict, time: float, cycle: int, difference: int, is_diverse: int,
                         summations: list, expirations: list):
        output = pow(4, obj["factory_level"]) * pow(2, obj["output_level"])
        max_storage = difference + summations[3]
        actual_cycle = min(90, int((time - obj["last_produce"]) // cycle))
        for _ in range(actual_cycle):
            if (summations[0] >= max_storage * 5 * pow(4, is_diverse)
                    and summations[1] >= max_storage * 2 * pow(4, is_diverse)
                    and summations[2] >= max_storage * pow(4, is_diverse)):
                continue
            self._produce_single_material(obj, output, summations, expirations)

    def _produce_single_material(self, obj: dict, output: int, summations: list, expirations: list):
        materials = ["flour", "egg", "yeast"]
        for i, material in enumerate(materials):
            amount = random.randint(1, output * (5 if material == "flour" else 2 if material == "egg" else 1))
            r = self._generate_batch_id("materialbatch")
            self._add_to_batch(material, r, obj["groupid"], amount, expirations[i])
            summations[i] += amount

    # 生产面包
    def produce_bread(self, obj: dict, time: float, cycle: int, summations: list, is_diverse: int):
        bread_expiration = obj["bread_expiration"]
        output = pow(4, obj["factory_level"]) * pow(2, obj["output_level"])
        max_storage = 64 * pow(4, obj["factory_level"]) * pow(2, obj["storage_level"])
        actual_cycle = min(90, int((time - obj["last_produce"]) // cycle))
        for _ in range(actual_cycle):
            if summations[3] >= max_storage:
                continue
            self._produce_single_bread(obj, output, is_diverse, summations, bread_expiration)

    def _produce_single_bread(self, obj: dict, output: int, is_diverse: int, summations: list, bread_expiration: int):
        max_output = min(64, output)
        produced = random.randint(0, max_output) * pow(4, is_diverse)
        if produced > 0:
            self._add_to_batch("breadbatch", self._generate_batch_id("breadbatch"),
                               obj["groupid"], produced, bread_expiration)
        summations[3] += produced

        # 消耗材料
        self._consume_material(obj, "flour", summations, produced * 5, is_diverse)
        self._consume_material(obj, "egg", summations, produced * 2, is_diverse)
        self._consume_material(obj, "yeast", summations, produced, is_diverse)

    def _consume_material(self, obj: dict, material_type: str, summations: list, amount: int, is_diverse: int):
        material_batch = self.datautil.lookup("materialbatch", f"groupid_{obj['groupid']}")
        self._use_batch(material_type, material_batch, amount * pow(4, is_diverse))
        summations[0 if material_type == "flour" else 1 if material_type == "egg" else 2] -= amount * pow(4, is_diverse)


def execute(group_id: str):
    datautil = factory.DataUtilFactory.create_data_util()
    processor = BatchProcessor(datautil)
    time_now = datetime.datetime.now().timestamp()

    # 获取所有批次
    material_batch = datautil.lookup("materialbatch", f"groupid_{group_id}")
    bread_batch = datautil.lookup("breadbatch", f"groupid_{group_id}")

    # 定义总和
    summations = [sum([x['amount'] for x in material_batch if x['type'] == t]) for t in ["flour", "egg", "yeast"]]
    summations.append(sum([x['amount'] for x in bread_batch]))

    # 获取面包厂信息
    obj1 = datautil.lookup("breadfactory", f"groupid_{group_id}")[0]

    # 判断是不是无限供应
    if "infinite" not in obj1["supply_mode"]:
        cycle = 300 - 20 * (obj1["factory_level"] - 1) - 10 * obj1["speed_level"]
        difference = 64 * pow(4, obj1["factory_level"]) * pow(2, obj1["storage_level"]) - summations[3]
        is_diverse = obj1["supply_mode"] == "diverse"

        if (time_now - obj1["last_produce"]) // cycle >= 1:
            processor.produce_material(obj1, time_now, cycle, difference, is_diverse, summations,
                                       [obj1["flour_expiration"], obj1["egg_expiration"], obj1["yeast_expiration"]])
            processor.produce_bread(obj1, time_now, cycle, summations, is_diverse)

        last_produce = obj1["last_produce"] + floor((time_now - obj1["last_produce"]) / cycle) * cycle
        datautil.modify("breadfactory", f"groupid_{group_id}", {"last_produce": last_produce})
    else:
        datautil.modify("breadfactory", f"groupid_{group_id}", {"last_produce": time_now})
