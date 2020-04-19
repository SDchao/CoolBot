import nonebot
from .nmslApi import get_new_line
from .config import *
import sdchaos.plugins.permission_check as checker

@nonebot.on_command("nmsl", aliases=["骂人","对线"])
async def _(session : nonebot.CommandSession):
    if(checker.permission_check(session.ctx,GROUP_LIST,PRIVATE_LIST)):
        reply_msg = get_new_line()
        await session.send(reply_msg)

@nonebot.on_natural_language(keywords=["骂","对线","嘴臭","祖安","罗东旭","ldx"])
async def _(session : nonebot.NLPSession):
    return nonebot.IntentCommand(90.0,"nmsl")