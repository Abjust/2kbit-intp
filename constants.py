import datetime

import ruamel


# 全局常量，请勿删除此文件
class BotConstants:
    log_level: str = None
    bot_qq: int = None
    owner_qq: int = None
    command_prefix: str = None
    command_separator: str = None
    db_type: str = None
    db_host: str = None
    db_port: str = None
    db_user: str = None
    db_password: str = None
    db_name: str = None
    boot_time: int = None

    @classmethod
    def initialize(cls, config_file):
        with open(config_file, 'r') as f:
            config_data = ruamel.yaml.load(f)
        for key, value in config_data.items():
            if key in ["owner_qq", "bot_qq", "db_port"]:
                setattr(cls, key, int(value))
            else:
                setattr(cls, key, value)
        cls.set_boot_time()

    @classmethod
    def set_boot_time(cls):
        time_now = datetime.datetime.now().timestamp()
        BotConstants.boot_time = time_now
