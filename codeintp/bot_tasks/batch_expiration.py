import datetime

from codeintp.bot_utils.datautil import factory


def delete_expired_batches(batch_type: str, group_id: str, time_now: float, datautil):
    batch = datautil.lookup(batch_type, f"groupid_{group_id}")
    expired_batch = [x for x in batch if x['expiry'] != 0 and time_now >= x['expiry']]
    for batch in expired_batch:
        datautil.delete(batch_type, f"batchid_{batch['batchid']}")


def execute(group_id: str):
    time_now = datetime.datetime.now().timestamp()
    datautil = factory.DataUtilFactory.create_data_util()

    delete_expired_batches("materialbatch", group_id, time_now, datautil)
    delete_expired_batches("breadbatch", group_id, time_now, datautil)
