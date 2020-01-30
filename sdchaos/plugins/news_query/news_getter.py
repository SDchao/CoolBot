from os import path
from datetime import datetime
from datetime import timedelta
import requests


def get_news(provience: str, hour = "24") -> list:
    url = "https://file1.dxycdn.com/2020/0127/794/3393185296027391740-115.json"
    respone = requests.get(url)
    j = respone.json()

    rList = []

    # 请求未成功
    if(j["code"] != "success"):
        return rList

    j = j["data"]

    for newsObject in j:
        if("provinceName" in newsObject):
            now_province_name : str  = newsObject["provinceName"]
            # 若为目标省份
            if(now_province_name.find(provience) != -1):
                # 获取发布时间
                pubDate : int = newsObject["pubDate"]
                pubDateTime = datetime.fromtimestamp(pubDate / 1000)
                deltaPub = datetime.now() - pubDateTime
                requireDelta = timedelta(hours= int(hour))
                
                if  deltaPub < requireDelta:
                    rList.append(_combine_news(newsObject))
                else:
                    # 已经发现超时新闻，不在继续
                    break
    return rList


def _combine_news(newsObject) -> str:
    result = newsObject["pubDateStr"]
    result += "\n" + newsObject["title"]
    result += "\n来自 " + newsObject["infoSource"]
    return result


if __name__ == "__main__":
    get_news("安徽", hour=24)
