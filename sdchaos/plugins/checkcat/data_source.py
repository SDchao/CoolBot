import requests
import base64
from PIL import Image
from nonebot import logger
from nonebot.typing import Context_T
from io import BytesIO

from .config import *

async def animalInPic(picUrl : str) -> str:
    access_token : str = await _getAccessToken()       
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal?access_token=" + access_token
    try:
        pic_respone = requests.get(picUrl)
        img = Image.open(BytesIO(pic_respone.content)).convert("RGB")
        output_buffer = BytesIO()
        img.save(output_buffer, format="JPEG")
        byte_data = output_buffer.getvalue()
        b64_str = base64.b64encode(byte_data)
        # img = base64.b64encode(pic_respone.content)
        params = {"image" : b64_str}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if(response):
            j = response.json()
            logger.debug(j)      
            animalName : str = j["result"][0]["name"]
            return animalName
    except BaseException as err:
        logger.error(err)
        return None
        

        
async def _getAccessToken() -> str:
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=yG8fLxI3bAxaBp6QKerSEcmV&client_secret=0XDMuMKQUP7u4n4q5kUZ3lEG7HSIZliA'
    response = requests.get(host)
    if response:
        j = response.json()
        return j["access_token"]
        
def isAllowTo(ctx : Context_T) -> bool :
    if(ctx["post_type"] == "message") :
        if(ctx["message_type"] == "group") :
            if(ctx["group_id"] in GROUP_LIST) :
                return True
        elif(ctx["message_type"] == "private"):
            if(ctx["user_id"] in PRIVATE_LIST) :
                return True

    return False