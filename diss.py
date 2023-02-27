from pyrogram import Client
from config import command, GlobalSN

import aiohttp

@Client.on_message(command('diss'), group=GlobalSN.reg(locals(), 'cmd', 'diss', '怼人', None, '0.1'))
async def handler(client, message):
    await message.delete()
    reply = message.reply_to_message_id if message.reply_to_message_id else None
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zuan.shabi.workers.dev') as resp:
            if resp.status == 200:
                text = f'**{await resp.text("utf-8")}**'
                if reply:
                    text += f' [😘](tg://user?id={message.reply_to_message.from_user.id})'
                await client.send_message(message.chat.id, text, reply_to_message_id=reply)
