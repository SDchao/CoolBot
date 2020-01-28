from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from datetime import datetime
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot import logger
from os import path
from .data_source import animalInPic
from .data_source import isAllowTo

totalCatCount : int = 0
catSavePath = path.join(path.dirname(__file__),"totalCatCount.txt")  

@on_command("checkCat")
async def checkCat(session : CommandSession):
    picUrlList = session.get("picList")
    hasCat : bool = False
    name : str = None
    global totalCatCount
    global catSavePath

    if(path.exists(catSavePath)):
        saveFile = open(catSavePath,"r")
        totalCatCount = int(saveFile.read())
        logger.debug("Loaded CatCount: " + str(totalCatCount))

    for picUrl in picUrlList:  
        name = await animalInPic(picUrl)      
        if(name and name.find("猫") != -1):
            totalCatCount += 1
            hasCat = True
    
    if(hasCat):
        await session.send(f"您刚刚发送了一只{name}\n今日猫图：{totalCatCount}")
        saveFile = open(catSavePath,"w")
        saveFile.write(str(totalCatCount))
        saveFile.close()


@on_natural_language(only_to_me = False)
async def _(session : NLPSession):
    # if (not isAllowTo(session.ctx)):
    #    return
    if session.msg_images:
        return IntentCommand(80.0, 'checkCat', args = {"picList": session.msg_images})

@nonebot.scheduler.scheduled_job("cron", day="*")
async def _():
    try:
        bot = nonebot.get_bot()
        global catSavePath
        saveFile = open(catSavePath,"r")
        totalCatCount = int(saveFile.read())
        saveFile.close()
        await bot.send_group_msg(group_id = 796439009,message = f"今天群友们一共发送了{totalCatCount}张猫图\n明天也要继续努力哦")
    except CQHttpError as err:
        print(type(err))