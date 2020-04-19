from os import path

import nonebot
import config

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugin("sdchaos.plugin.nmsl")
    nonebot.run(host="127.0.0.1", port=8081)
