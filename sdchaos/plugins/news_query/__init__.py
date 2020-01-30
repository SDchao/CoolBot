from nonebot import on_command, CommandSession
from .import news_getter
from .import checker

__plugin_name__ = "肺炎新闻查询"
__plugin_usage__ = r"""
有关肺炎新闻查询

news [省份名称] [发布经过的小时]

例如:
news 安徽 10
"""


@on_command("news", aliases=["新闻", "要闻", "n"])
async def news(session: CommandSession):
    global __plugin_usage__    
    if not checker.isAllowTo(session.ctx):
        return

    if session.current_arg == "" :
        await session.send(__plugin_usage__)
    else :
        arg_list = session.current_arg.split(" ")
        news_list: list = []
        if len(arg_list) == 1:
            news_list = news_getter.get_news(arg_list[0])
        else :
            news_list = news_getter.get_news(arg_list[0], arg_list[1])
            if len(news_list) == 0:
                await session.send("欸，没有找到有关报道呐\n暂不支持城市查询呐")
                return
        for newsMsg in news_list :
            await session.send(newsMsg)