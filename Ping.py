from pyrogram import Client
from config import command, GlobalSN, Packages, prefixes

from datetime import datetime
from pyrogram.raw.functions import Ping

if Packages('ping3'):
    from ping3 import ping

doc = f"1、`{prefixes}ping`\n2、`{prefixes}ping dc`"

@Client.on_message(command('ping'), group=GlobalSN.reg(locals(), 'cmd', 'ping', 'ping', doc))
async def handler(client, message):
    args = message.text.strip().split()
    arg = args[1] if len(args) > 1 else None
    if arg == 'dc':
        await message.edit("ping...")
        DCs = {
            1: "149.154.175.53",
            2: "149.154.167.51",
            3: "149.154.175.100",
            4: "149.154.167.91",
            5: "91.108.56.130"
        }

        data = []
        for dc in range(1, 6):
            result = round(ping(DCs[dc], unit = "ms"), 2)
            data.append(result)

        if not any(data):
            await message.edit("ping 失败~")
            return

        await message.edit(
            f"🇺🇸 `DC1`: `{data[0]}ms`\n"
            f"🇳🇱 `DC2`: `{data[1]}ms`\n"
            f"🇺🇸 `DC3`: `{data[2]}ms`\n"
            f"🇳🇱 `DC4`: `{data[3]}ms`\n"
            f"🇸🇬 `DC5`: `{data[4]}ms`\n")    

    else:
        #https://github.com/TeamPGM/PagerMaid-Pyro/blob/aff6d953a1e00dc2241db9da32abc8f4c45453d3/pagermaid/modules/status.py#L126
        start = datetime.now()
        await client.invoke(Ping(ping_id=0))
        end = datetime.now()
        ping_duration = (end - start).microseconds / 1000
        start = datetime.now()
        await message.edit("Pong!")
        end = datetime.now()
        msg_duration = (end - start).microseconds / 1000
        await message.edit(f"Pong!| PING: {ping_duration}ms | MSG: {msg_duration}ms")
