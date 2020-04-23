import nonebot
import random

COMPLETE_TEXT = ("那当然是&item&啦！", "不妨选择&item&", "肯定要&item&", "我觉得应该&item&")


@nonebot.on_command("roll", aliases=["r"])
async def roll(session: nonebot.CommandSession):
    itemList = session.get("items", prompt="请输入选项，用空格间隔开哦")
    if(len(itemList) < 2):
        session.finish("不可以只Roll一个东西啊！坏蛋")
    else:
        randomIndex = random.randint(0, len(itemList) - 1)
        selected = itemList[randomIndex]
        reMsg = _get_complete_text(selected)
        await session.send(reMsg)



@roll.args_parser
async def _(session: nonebot.CommandSession):
    arg = session.current_arg_text.strip()
    if arg:
        # 将arg按空格拆分为随机item
        tmpList = arg.split(" ")
        itemList = list(set(tmpList))

        # 若有重复项
        if(len(itemList) < len(tmpList)):
            session.send("居然有重复！帮你去掉了啊坏蛋")
        session.state["items"] = itemList
    elif not session.is_first_run:
        # 若不是第一次询问且还是没有参数
        session.finish("你这不是啥都没有输入嘛……")

@nonebot.on_natural_language(keywords=["选", "挑", "猜", "随便"])
async def _(session: nonebot.NLPSession):
    arg = _get_nlp_arg(session.msg_text)
    return nonebot.IntentCommand(70, "roll", current_arg=arg or "")


@nonebot.on_natural_language(keywords=["随机", "帮我选", "帮我挑"])
async def _(session: nonebot.NLPSession):
    arg = _get_nlp_arg(session.msg_text)
    return nonebot.IntentCommand(85, "roll", current_arg=arg or "")


def _get_nlp_arg(rawMsg: str) -> str:
    """获取NLP关键词命中后的参数

    Returns:
        返回语句所含参数，若无法解析则返回None
    """
    rawMsg = rawMsg.strip()
    # 将rawMsg按空格分割
    msgList = rawMsg.split(" ", 1)

    # 若消息只有1节
    if(len(msgList) < 2):
        return None
    else:
        return msgList[1]


def _get_complete_text(selected: str) -> str:
    global COMPLETE_TEXT
    randomIndex = random.randint(0, len(COMPLETE_TEXT) - 1)
    return COMPLETE_TEXT[randomIndex].replace("&item&", selected)
