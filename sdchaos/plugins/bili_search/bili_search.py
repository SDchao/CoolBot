import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

SEARCH_URL = "https://search.bilibili.com/all?keyword=%keyword%"


def search(title: str) -> str:
    '''
    获取对应标题的bilibili视频链接

    Returns:
        返回视频链接，若无结果返回None
        若出现错误则返回对应描述字符串
    '''

    # 若不包含Title，返回空
    if not title:
        return None

    global SEARCH_URL
    # 要查询的链接
    url = SEARCH_URL.replace("%keyword%", quote(title, "utf-8"))
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64"}
    respone = requests.get(url=url, headers=headers)
    if (respone.status_code == 412):
        return "访问过于频繁，无法获取内容……"
    elif (respone.status_code != 200):
        return "访问出现" + respone.status_code + "错误"
    else:
        # 成功获取内容
        content = respone.text
        info = _analysis_video(content, title)

        if not info:
            # 若没有相关信息则返回None
            return None
        else:
            # 找到对应标题视频
            msg = \
                info["title"] + "\n" + \
                "播放 " + info["watched"] + " 弹幕 " + info["damu"] + " " + info["time"] + "\n" + \
                "Up主 " + info["up"] + "\n" + \
                info["url"]

            return msg


def _analysis_video(content: str, target_title: str) -> dict:
    soup = BeautifulSoup(content, features="html5lib")
    # 获取视频父
    videoParent: BeautifulSoup = soup.find("ul", attrs={"type": "video", "class": "video-list clearfix"})
    for video in videoParent.find_all("li", class_="video-item"):
        # 遍历视频的title
        title = video.a["title"]
        # if(title == target_title):
        # 不要求准确标题
        if (True):
            # 发现目标视频
            tags = video.find("div", class_="tags").find_all("span")
            ret: dict = {}

            ret["url"] = "https:" + str(video.a["href"]).replace("?from=search", "")

            ret["title"] = str(video.a["title"]).strip()
            ret["watched"] = str(tags[0].text).strip()
            ret["damu"] = str(tags[1].text).strip()
            ret["time"] = str(tags[2].text).strip()
            ret["up"] = str(tags[3].text).strip()

            return ret
    return None


if __name__ == "__main__":
    print(search("JOJO历代BOSS主题曲（Themes）1~5部"))
