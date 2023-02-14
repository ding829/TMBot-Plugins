from client.utils import OnDraft
from pyrogram import enums
import asyncio

@OnDraft("admin", help="召唤管理员")
async def handler(client, update, chat_id, args, reply):
    if reply:
        text = str()
        async for m in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not m.user.is_bot:
                text += f'{m.user.mention(style="md")}\n'
        if text:
            msg = await client.send_message(chat_id, text, reply_to_message_id=reply)
            try:
                for i in range(120):
                    await asyncio.sleep(5)
                    if (await client.get_messages(chat_id, reply)).empty:
                        await msg.delete()
            except Exception as e:
                pass