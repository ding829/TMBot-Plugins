from client.utils import OnDraft

doc="默认为复读机，添加 save 为转发到 Saved Messages"

@OnDraft("re", help="复读机或一键收藏", doc=doc)
async def handler(client, update, chat_id, args, reply):
    from_chat_id = chat_id
    chat_id = "me" if len(args) >= 1 and args[0] == "save" else chat_id
    try:
        await client.forward_messages(chat_id, from_chat_id, reply)
    except Exception as e:
        try:
            await client.copy_message(chat_id, from_chat_id, reply)
        except Exception as e:
            pass
