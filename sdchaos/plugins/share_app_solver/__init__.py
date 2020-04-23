import nonebot
import json
import re
import asyncio
from nonebot import logger

@nonebot.on_command("_solve_app")
async def _solve_app(session : nonebot.CommandSession):
    if(session.current_arg):
        newsObj = json.loads(session.current_arg)
        logger.debug(newsObj)
        title : str = newsObj["title"]
        url : str = newsObj["jumpUrl"]
        imageUrl : str = newsObj["preview"]
        imageCq = nonebot.MessageSegment(type_="image", data={"file":imageUrl})
        msg = nonebot.Message(title + "\n")
        msg.append(imageCq)
        msg.extend(url)
        await session.send(msg)


@nonebot.on_natural_language(only_to_me= False, only_short_message= False)
async def _solve_app_nlp(session : nonebot.NLPSession):
    logger.log(0, session.msg)
    msg_raw = session.msg
    if(msg_raw.find("哔哩哔哩") != -1):
        content : str = re.match('\[CQ:rich,content={"news":(.*)}', msg_raw).group(1)
        content = content.replace("&amp;#44;",",")
        return nonebot.IntentCommand(100, "_solve_app", current_arg=content)