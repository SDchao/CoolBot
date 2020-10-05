from nonebot.typing import Context_T


def permission_check(ctx: Context_T = None, group_list: tuple = (), private_list: tuple = ("*",)) -> bool:
    if (ctx):
        if ctx["post_type"] == "message":
            if (ctx["message_type"] == "group"):
                if (ctx["group_id"] in group_list):
                    return True
            elif (ctx["message_type"] == "private"):
                if ("*" in private_list or ctx["user_id"] in private_list):
                    return True

    return False
