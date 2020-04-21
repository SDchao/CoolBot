from os import path

import nonebot
import config

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugin("sdchaos.plugins.nmsl")
    nonebot.load_plugin("sdchaos.plugins.roll")
    nonebot.run(host="127.0.0.1", port=8081)
