from client.utils import OnDraft
from pyrogram import enums

@OnDraft("ban", help="滥权")
async def handler(client, update, chat_id, args, reply):
    if reply:
        msg = await client.get_messages(chat_id, update.draft.reply_to_msg_id)
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
