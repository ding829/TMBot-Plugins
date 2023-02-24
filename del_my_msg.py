from pyrogram import Client, enums
from config import command, GlobalSN, prefixes

import asyncio

def is_number(s):
    try:
        val = int(s)
        if val > 0:
            return True
    except:
        return False 

doc = f"""1、默认删除十条消息：`{prefixes}dme`
2、删除 N 条消息：`{prefixes}dme N`
3、删除所有群的消息：`{prefixes}dme all`
"""

@Client.on_message(command('dme'), group=GlobalSN.reg(locals(), 'cmd', 'dme', '删除自己的消息', doc))
async def handler(client, message):
    await message.delete()

    chat_id = message.chat.id

    args = message.text.strip().split()
    arg = args[1] if len(args) > 1 else None

    async def dmlmsg(msg):
        if not msg.service:
            try:
                if msg.text or msg.caption:
                    await msg.edit_text('ㅤ')
            except:
                pass
            try:
                await msg.delete()
            except:
                pass

    if arg == "all":
        async for dialog in client.get_dialogs():
            if dialog.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP}:
                async for msg in client.search_messages(dialog.chat.id, from_user="me"):
                    await dmlmsg(msg)
    else:
        if is_number(arg):
            limit = int(arg)
        else:
            limit = 10
        async for msg in client.search_messages(chat_id, from_user="me", limit=limit):
            await dmlmsg(msg)
