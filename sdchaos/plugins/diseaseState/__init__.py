from nonebot import on_command, CommandSession
from nonebot import logger

from .checker import CheckArea
from .checker import isAllowTo
from .checker import getNews
from .config import GROUP_LIST

import nonebot
from aiocqhttp.exceptions import Error as CQHttpError


@on_command("ds", aliases=("查询","疫情"))
async def checkState(session: CommandSession):
    if not isAllowTo(session.ctx):
        return
    argList = session.current_arg.split(" ")
    result: str = None
    if(len(argList) == 1):
        result = CheckArea(argList[0])
    elif(len(argList) == 2):
        result = CheckArea(argList[0], city=argList[1])
    if(result):
        await session.send(result)


@nonebot.scheduler.scheduled_job("interval", minutes=1)
async def _():
    logger.info("即将尝试推送新闻")
    newsList = getNews()
    logger.info(newsList)
    bot = nonebot.get_bot()
    try:
        for news in newsList:
            for group in GROUP_LIST:
                await bot.send_group_msg(group_id=group, message=news)
    except CQHttpError:
        logger.error("发送疾病新闻失败")
