import nonebot
import json
import re
import asyncio
from nonebot import logger

from .bili_search import search

@nonebot.on_command("_solve_app")
async def _solve_app(session : nonebot.CommandSession):
    if(session.current_arg):
        msg_raw = session.current_arg
        # 进行转义并规范为json
        msg = msg_raw.replace("&amp;#44;", ",").replace("&amp;#91;","[").replace("&amp;#93;","]")
        if(msg.find("title=[QQ小程序]哔哩哔哩") != -1):
            # 若为哔哩哔哩小程序
            content = re.match("\[CQ:rich,content=(.*),")
            if content:
                content = content.group(1)
                contentObj = json.loads(content)

                title = contentObj["desc"]

                msg = search(title)
                await session.send(msg)

        


@nonebot.on_natural_language(only_to_me= False, only_short_message= False)
async def _solve_app_nlp(session : nonebot.NLPSession):
    msg_raw = session.msg
    if(msg_raw.find("CQ:rich") != -1 and msg_raw.find("QQ小程序") != -1):
        # 发现小程序
        return nonebot.IntentCommand(100.0, "_solve_app", current_arg = msg_raw)