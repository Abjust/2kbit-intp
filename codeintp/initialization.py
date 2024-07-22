from codeintp.bot_utils import permission, turned_off, scheduler


def execute():
    # 初始化权限模块缓存
    permission.initialize_cache()
    # 初始化开关模块缓存
    turned_off.initialize()
    # 初始化定时任务
    scheduler.update_schedules("initialize")
