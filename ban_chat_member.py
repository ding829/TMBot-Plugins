from pyrogram import Client, enums
from config import command, GlobalSN

from pyrogram import enums

@Client.on_message(command('ban'), group=GlobalSN.reg(locals(), 'cmd', 'ban', '滥权', None, '0.2'))
async def handler(client, message):
    await message.delete()
    reply = message.reply_to_message_id if message.reply_to_message_id else None
    
    async def ban(chat_id, user_id):
        status = (await client.get_chat_member(chat_id, "me")).status
        if status in {enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR}:
            try:
                await client.ban_chat_member(chat_id, user_id)
            except Exception:
                pass
            try:
                await client.delete_user_history(chat_id, user_id)
            except Exception:
                pass

    if reply:
        msg = await client.get_messages(message.chat.id, reply)
        await ban(message.chat.id, msg.from_user.id)

        chats = await client.get_common_chats(msg.from_user.id)
        for chat in chats:
            await ban(chat.id, msg.from_user.id)
