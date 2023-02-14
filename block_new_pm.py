from client.utils import OnMsg
from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory

@OnMsg(help="自动封禁无聊天记录的私聊", filters=filters.private)
async def handler(client, msg):
    message = await client.get_messages(msg.chat.id, msg.id)
    if not bool(msg.from_user and (msg.from_user.is_self or msg.outgoing)):
        if await client.search_messages_count(msg.chat.id) <= 1:
            await client.read_chat_history(msg.chat.id)
            await client.invoke(
                DeleteHistory(
                    max_id=0, 
                    revoke=True, 
                    peer=(await client.resolve_peer(msg.from_user.id))
                )
            )
            await client.block_user(msg.from_user.id)
