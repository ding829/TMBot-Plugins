from config import GlobalSN, app

from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory

onmsg = filters.private & ~filters.me

@Client.on_message(onmsg, group=GlobalSN.reg(locals(), 'msg', None, '封禁无记录私聊', None, '0.1'))
async def handler(client, message):
    if await client.search_messages_count(message.chat.id) <= 1:
        await client.read_chat_history(message.chat.id)
        await client.invoke(
            DeleteHistory(
                max_id=0, 
                revoke=True, 
                peer=(await client.resolve_peer(message.from_user.id))
            )
        )
        await client.block_user(message.from_user.id)
