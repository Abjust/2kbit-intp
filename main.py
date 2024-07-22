import os.path
import sys
from textwrap import dedent

import nonebot
import ruamel.yaml
from loguru import logger
from nonebot import require
from nonebot.adapters.onebot import V11Adapter

import constants
from codeintp.bot_utils.logger import bot_logger

# 初始化
host_addr = ""
if not os.path.exists("config.yaml"):
    config_yaml = """\
    # 日志等级，分为trace、debug、info、success、warning、error和critical
    log_level: 'info'
    # 指令前缀
    command_prefix: '!'
    # 指令分隔符
    command_separator: '.'
    # onebot-api连接地址，如果没有动就不需要改
    host_addr: "127.0.0.1:8080"
    # 机器人主人QQ号
    owner_qq: 0
    # 机器人QQ号
    bot_qq: 0
    # 数据存储方法，可以是mysql、sqlite、json或者yaml
    db_type: 'json'
    # 数据库主机，仅mysql需要，其他可以留空
    db_host: ''
    # 数据库端口，仅mysql需要，其他可以不动
    db_port: 3306
    # 数据库用户，仅mysql需要，其他可以留空
    db_user: ''
    # 数据库密码，仅mysql需要，其他可以留空
    db_password: ''
    # 数据库名称，仅mysql需要，其他可以留空
    db_name: ''
    """
    with open('config.yaml', 'w', encoding='utf-8') as file:
        file.write(dedent(config_yaml))
    input("配置文件已创建！现在，你需要前往项目文件夹或者程序文件夹找到config.yml并按照要求编辑（按回车键退出）")
    exit(0)
else:
    accepted_type = [
        "mysql",
        "sqlite",
        "json",
        "yaml"
    ]
    accepted_level = [
        "trace",
        "debug",
        "info",
        "success",
        "warning",
        "error",
        "critical"
    ]
    with open('config.yaml', 'r', encoding='utf-8') as file:
        yaml = ruamel.yaml.YAML()
        config_yaml = yaml.load(file)
        host_addr = str(config_yaml["host_addr"]).split(":")
        if config_yaml["log_level"].lower() not in accepted_level:
            logger.error(f"请正确填写日志等级！仅接受{accepted_level}\n")
            input("按回车键关闭")
            exit(1)
        if config_yaml["db_type"].lower() not in accepted_type:
            logger.error(f"请正确填写存储方法！仅接受{accepted_type}\n")
            input("按回车键关闭")
            exit(1)
        constants.BotConstants.initialize(file.name)

# 设置日志
bot_logger.remove()
log_level = constants.BotConstants.log_level.upper()
bot_logger.add(sys.stderr, level=log_level)
bot_logger.add("log_file.log", level=log_level)

# 初始化机器人程序
nonebot.init(host=host_addr[0], port=host_addr[1], driver="~fastapi",
             log_level=log_level,
             superusers={constants.BotConstants.owner_qq},
             command_start={constants.BotConstants.command_prefix},
             command_sep={constants.BotConstants.command_separator})
driver = nonebot.get_driver()
driver.register_adapter(V11Adapter)
require("nonebot_plugin_alconna")
require("nonebot_plugin_apscheduler")

# 加载插件
for root, dirs, files in os.walk("codeintp/modules", topdown=False):
    for name in files:
        module = os.path.join(root, name).replace('\\', '.').replace('./', '').replace('/', '.').split('.')
        if module[-2].startswith("_"):
            continue
        module = '.'.join(module)[:-3]
        if '__pycache__' in module:
            continue
        bot_logger.info(f'{module} 将被载入')
        nonebot.load_plugin(module)
        bot_logger.info(f"name: {nonebot.get_plugin_by_module_name(module).metadata.name}")
        bot_logger.info(f"description: {nonebot.get_plugin_by_module_name(module).metadata.description}")

# 启动！
bot_logger.success('恭喜！启动成功，0Error，至少目前如此，也祝你以后如此')

if __name__ == "__main__":
    nonebot.run()
