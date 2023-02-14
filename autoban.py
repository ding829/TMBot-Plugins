from client.utils import OnMsg
from client.config import logger
from pyrogram import filters, enums
from pyrogram.raw.functions.messages import DeleteHistory

keys = 'IP2World|小馬拉大車 ➕|人獸 ➕|接各种资金|卡接回U|ip2world|同台出U|全国同台|大量下浮出U|接黑白资|下浮U|一手U商|呦呦|人獸|呦女|呦 呦|需代收。请滴滴'

@OnMsg(help="关键字自动滥权", filters=filters.regex(keys))
async def handler(client, msg):
    chats = await client.get_common_chats(msg.from_user.id)
    for chat in chats:
        status = (await client.get_chat_member(chat.id, "me")).status
        if status in {enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR}:
            try:
                await client.ban_chat_member(chat.id, msg.from_user.id)
                await client.delete_user_history(chat.id, msg.from_user.id)
            except:
                pass
