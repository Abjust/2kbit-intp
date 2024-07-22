from arclet.alconna import Alconna, Args, Arparma
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="复读",
    description="人类的本质是复读机",
    usage=""
)

echo = on_alconna(
    Alconna("echo",
            Args["text", str]),
    priority=10,
    use_cmd_start=True
)


@echo.handle()
async def handle_function(result: Arparma):
    if "echo" not in result.query("text"):
        await echo.finish(result.query("text"))
