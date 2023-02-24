from pyrogram import Client, enums
from config import command, GlobalSN

from pyrogram import enums

@Client.on_message(command('ban'), group=GlobalSN.reg(locals(), 'cmd', 'ban', '滥权'))
async def handler(client, message):
    await message.delete()
    reply = message.reply_to_message_id if message.reply_to_message_id else None
    chat_id = message.chat.id
    if reply:
        msg = await client.get_messages(chat_id, reply)
        chats = await client.get_common_chats(msg.from_user.id)
        for chat in chats:
            status = (await client.get_chat_member(chat.id, "me")).status
            if status in {enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR}:
                try:
                    await client.ban_chat_member(chat.id, msg.from_user.id)
                except:
                    pass
                try:
                    await client.delete_user_history(chat.id, msg.from_user.id)
                except:
                    pass
