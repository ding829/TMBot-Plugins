from client.utils import OnDraft
from client.config import prefix
from pyrogram import enums

doc = f"""1、默认删除十条消息：`{prefix}dme`
2、删除 N 条消息：`{prefix}dme N`
3、删除所有群的消息：`{prefix}dme all`
"""

def is_number(s):
    try:
        val = int(s)
        if val > 0:
            return True
    except:
        return False 

@OnDraft("dme", help="删除自己的消息",doc=doc)
async def handler(client, update, chat_id, args, reply):
    async def dmlmsg(m):
        if not message.service:
            try:
                if message.text or message.caption:
                    await message.edit_text('ㅤ')
            except:
                pass

            try:
                await message.delete()
            except:
                pass

    if args and args[0] == "all":
        async for dialog in client.get_dialogs():
            if dialog.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP}:
                async for message in client.search_messages(dialog.chat.id, from_user="me"):
                    await dmlmsg(message)
    else:
        if args and is_number(args[0]):
            limit = int(args[0])
        else:
            limit = 10
        async for message in client.search_messages(chat_id, from_user="me", limit=limit):
            await dmlmsg(message)
