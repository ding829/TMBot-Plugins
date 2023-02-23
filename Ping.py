from client.utils import OnCmd
from client.config import prefix

from datetime import datetime
from pyrogram.raw.functions import Ping
from ping3 import ping

PIP = 'ping3'

doc = f"1、`{prefix}ping`\n2、`{prefix}ping dc`"

@OnCmd("ping", help="ping", doc=doc)
async def handler(client, msg, chat_id, args, reply):
    arg = args[0] if len(args) >= 1 else None
    if arg == 'dc':
        await msg.edit("ping...")
        DCs = {
            1: "149.154.175.53",
            2: "149.154.167.51",
            3: "149.154.175.100",
            4: "149.154.167.91",
            5: "91.108.56.130"
        }

        data = []
        for dc in range(1, 6):
            result = ping(DCs[dc], unit = "ms")
            data.append(result)

        if not any(data):
            await msg.edit("ping 失败~")
            return

        await msg.edit(
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
        await msg.edit("Pong!")
        end = datetime.now()
        msg_duration = (end - start).microseconds / 1000
        await msg.edit(f"Pong!| PING: {ping_duration}ms | MSG: {msg_duration}ms")
