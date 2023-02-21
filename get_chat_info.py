from client.utils import OnCmd
from pyrogram import enums

import datetime

@OnCmd("info", help="获取对话或者群员、群的信息")
async def handler(client, msg, chat_id, args, reply):
    await msg.edit("获取中...")
    
    user = None
    channel_id = None
    sender_chat_id = None
    get_chat_member = None

    def GetInfo(dicts):
        text = str()
        for i in dicts:
            if not isinstance(dicts[i], bool):
                if isinstance(dicts[i], (str, int, datetime.datetime, enums.ChatMemberStatus, enums.ChatType)):
                    if i != "phone_number":
                        if isinstance(dicts[i], (enums.ChatMemberStatus, enums.ChatType)):
                            text += f"**{i}**: `{dicts[i].value}`\n"
                        else:
                            text += f"**{i}**: `{dicts[i]}`\n"
        return text

    if bool(msg.chat and msg.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP}):
        channel_id = msg.chat.id
        if reply:
            if msg.reply_to_message.sender_chat:
                sender_chat_id = msg.reply_to_message.sender_chat.id
                get_sender_chat = (await client.get_chat(sender_chat_id)).__dict__
            else:
                user = msg.reply_to_message.from_user.id
                get_chat_member = (await client.get_chat_member(channel_id, user)).__dict__
        else:
            get_chat = (await client.get_chat(channel_id)).__dict__
    else:
        channel_id = msg.chat.id
        get_chat = (await client.get_chat(channel_id)).__dict__

    if user:
        get_user = (await client.get_users(user)).__dict__
        text = GetInfo(get_user)

    if channel_id and reply:
        if sender_chat_id:
            text = GetInfo(get_sender_chat)
        else:
            text += GetInfo(get_chat_member)
            messages_count = await client.search_messages_count(channel_id, from_user=user)
            text += f"**messages_count**: `{messages_count}`\n"
    elif channel_id and not reply:
        text = GetInfo(get_chat)
    else:
        text = "获取失败~"

    await msg.edit(text)
