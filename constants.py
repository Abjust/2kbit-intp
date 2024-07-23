import datetime

import ruamel


# 全局常量，请勿删除此文件
class BotConstants:
    log_level: str = ""
    bot_qq: int = 0
    owner_qq: int = 0
    command_prefix: str = ""
    command_separator: str = ""
    db_type: str = ""
    db_host: str = ""
    db_port: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    boot_time: int = 0

    @classmethod
    def initialize(cls, config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            yaml = ruamel.yaml.YAML()
            config_data = yaml.load(f)
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
