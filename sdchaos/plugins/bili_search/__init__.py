from .bili_search import search
import nonebot

@nonebot.on_command("search_b", aliases=("搜索B站", "B站视频", "搜索视频"))
async def search_b(session : nonebot.CommandSession):
    t = session.get("title", prompt="请输入要查找的视频标题")
    msg = search(t)
    await session.send(msg)

@search_b.args_parser
async def _(session : nonebot.CommandSession):
    arg = session.current_arg_text
    if arg :
        session.state["title"] = arg
    elif not session.is_first_run:
        session.finish("你这不是什么都没输入嘛")

@nonebot.on_natural_language(keywords={"搜索B站", "B站视频", "搜索b站", "b站视频", "搜索视频"})
async def _(session : nonebot.NLPSession):
    args = session.msg_text.strip().split(" ",1)
    arg = ""
    if len(args) > 1 :
        arg = args[1]
    return nonebot.IntentCommand(150, "search_b", current_arg= arg)