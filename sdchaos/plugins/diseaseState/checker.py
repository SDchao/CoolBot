import requests
from nonebot import logger
from nonebot.typing import Context_T
from os import path

from .config import *


def CheckArea(area: str, city: str = None) -> str:
    url: str = "http://49.232.173.220:3001/data/getAreaStat/"
    url += area
    provinceName = ""
    confirmedCount = ""
    suspectedCount = ""
    deadCount = ""
    curedCount = ""

    respone = requests.get(url)
    j = respone.json()
    # 查询无结果
    if len(j) == 0:
        return None
    else:
        j = j[0]
        provinceName = j["provinceName"]
        # 若只需要省份数据
        if not city:
            confirmedCount = j["confirmedCount"]
            suspectedCount = j["suspectedCount"]
            deadCount = j["deadCount"]
            curedCount = j["curedCount"]
            return _CombineResult(provinceName, confirmedCount, suspectedCount, deadCount, curedCount)
        else:
            # 获取全部城市
            cities = j["cities"]
            for c in cities:
                # 找到城市
                if c["cityName"] == city:
                    confirmedCount = c["confirmedCount"]
                    suspectedCount = c["suspectedCount"]
                    deadCount = c["deadCount"]
                    curedCount = c["curedCount"]
                    return _CombineResult(city, confirmedCount, suspectedCount, deadCount, curedCount)

    return None


def _CombineResult(area: str, confirmed: int, suspected: int, dead: int, cur: int):
    result = area + "疫情报告："
    if confirmed > 0:
        result += "\n感染人数：" + str(confirmed)
    if suspected > 0:
        result += "\n疑似病例：" + str(suspected)
    if dead > 0:
        result += "\n死亡人数：" + str(dead)
    if cur > 0:
        result += "\n治愈人数" + str(cur)
    return result

def isAllowTo(ctx : Context_T) -> bool :
    if(ctx["post_type"] == "message") :
        if(ctx["message_type"] == "group") :
            if(ctx["group_id"] in GROUP_LIST) :
                return True
        elif(ctx["message_type"] == "private"):
            if(ctx["user_id"] in PRIVATE_LIST) :
                return True

    return False

def getNews() -> list:
    lastId = "630"
    lastIdPath = path.join(path.dirname(__file__),"latestid.tmp")
    if(path.exists(lastIdPath)):
        f = open(lastIdPath,"r")
        lastId = f.read()
        f.close()
    
    url = "http://49.232.173.220:3001/data/getNewest/" + lastId
    respone = requests.get(url)
    j = respone.json()

    rList = []

    if len(j) == 0:
        return rList
    else:
        # 保存lastId
        lastId = str(j[0]["id"])
        f = open(lastIdPath,"w")
        f.write(lastId)
        f.close()

        for newsObject in j :
            rList.append(_CombineNews(newsObject))
        return rList

def _CombineNews(newsObject) -> str :
    result = newsObject["pubDateStr"]
    result += "\n" + newsObject["title"]
    result += "\n来自 " + newsObject["infoSource"]
    result += "\n" + newsObject["sourceUrl"]
    return result