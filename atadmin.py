from pyrogram import Client, enums
from config import command, GlobalSN

import asyncio

@Client.on_message(command('admin'), group=GlobalSN.reg(locals(), 'cmd', 'admin', '召唤管理员'))
async def handler(client, message):
    await message.delete()
    reply = message.reply_to_message_id if message.reply_to_message_id else None
    chat_id = message.chat.id
    if reply:
        text = str()
        async for m in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not m.user.is_bot:
                text += f'{m.user.mention(style="md")}\n'
        if text:
            message = await client.send_message(chat_id, text, reply_to_message_id=reply)
            try:
                for i in range(120):
                    await asyncio.sleep(5)
                    if (await client.get_messages(chat_id, reply)).empty:
                        await message.delete()
            except Exception as e:
                pass