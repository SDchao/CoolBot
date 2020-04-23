import nonebot

@nonebot.on_command("_solve_app")
async def _solve_app(session : nonebot.CommandSession):
    pass

@nonebot.on_natural_language(only_to_me= False, only_short_message= False)
async def _(session : nonebot.NLPSession):
    pass