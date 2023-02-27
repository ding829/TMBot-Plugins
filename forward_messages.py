from pyrogram import Client
from config import command, GlobalSN

doc="默认为复读机，添加 save 为转发到 Saved Messages"

@Client.on_message(command('re'), group=GlobalSN.reg(locals(), 'cmd', 're', '复读机', doc, '0.1'))
async def handler(client, message):
    await message.delete()
    args = message.text.strip().split()
    arg = args[1] if len(args) > 1 else None
    from_chat_id = message.chat.id
    chat_id = "me" if arg == "save" else from_chat_id
    try:
        await client.forward_messages(chat_id, from_chat_id, message.reply_to_message_id)
    except Exception as e:
        try:
            await client.copy_message(chat_id, from_chat_id, message.reply_to_message_id)
        except Exception as e:
            pass
