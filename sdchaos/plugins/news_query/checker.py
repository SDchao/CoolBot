from .config import *
from nonebot.typing import Context_T

def isAllowTo(ctx : Context_T) -> bool :
    if(ctx["post_type"] == "message") :
        if(ctx["message_type"] == "group") :
            if(ctx["group_id"] in GROUP_LIST) :
                return True
        elif(ctx["message_type"] == "private"):
            if(ctx["user_id"] in PRIVATE_LIST) :
                return True

    return False