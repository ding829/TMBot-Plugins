from config import GlobalSN, app

from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory

@Client.on_message(filters.private & ~filters.me, group=GlobalSN.reg(locals(), 'msg', None, '封禁无记录私聊', None, '0.2'))
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
