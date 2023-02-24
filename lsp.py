from pyrogram import Client, enums
from config import command, GlobalSN, Packages

import re
import random
import asyncio
from pyrogram.types import InputMediaPhoto

if Packages('requests'):
    import requests

doc = "参数：\n`pics`：套图\n`vid`：视频\n`mjx`：买家秀\n末尾添加 `s` 将启用防剧透功能"

@Client.on_message(command('lsp'), group=GlobalSN.reg(locals(), 'cmd', 'lsp', '来点色图', doc))
async def handler(client, message):
    await message.delete()
    args = message.text.strip().split()
    arg = args[1] if len(args) > 1 else None

    chat_id = message.chat.id
    reply = message.reply_to_message_id if message.reply_to_message_id else None

    has_spoiler = True if len(args) > 1 and args[-1] == 's' else False
    if has_spoiler == True:
        caption_has_spoiler = '||'
    else:
        caption_has_spoiler = ''

    types = args[1] if len(args) > 1 and args[1] in ['pics', 'vid', 'mjx'] else random.choice(['pics', 'vid', 'mjx'])

    if types == 'pics':
        url = None
        title = None
        img_urls = None

        channels = ["moretitok", "xiuren2021", "taotuxiezheng", "mrohome", "xz425"]

        for i in range(5):
            channel = random.choice(channels)
            count = await client.search_messages_count(chat_id=channel, filter=enums.MessagesFilter.URL)
            random_offset = random.randint(1, count)
            async for m in client.search_messages(chat_id=channel, offset=random_offset, limit=1, filter=enums.MessagesFilter.URL):
                if m.web_page:
                    url = m.web_page.url
                    res = requests.get(url=url)
                    title = m.web_page.title
                    img_urls = re.findall(r'<img [^>]*src="([^"]+)"[^>]*', res.text)
            if img_urls and title:
                break

        if img_urls and title:
            photos = img_urls
            if not (img_urls[0].startswith('http://') or img_urls[0].startswith('https://')):
                photos = ['https://telegra.ph/'+str(i) for i in img_urls]
            mesg = await client.send_photo(chat_id, photos[0], has_spoiler=has_spoiler, caption=f"{caption_has_spoiler}{title}{caption_has_spoiler}", reply_to_message_id=reply)
            del photos[0]
            try:
                for i, photo in enumerate(photos):
                    if i < len(photos):
                        await asyncio.sleep(5)
                        await client.edit_message_media(chat_id, mesg.id, InputMediaPhoto(photo, has_spoiler=has_spoiler, caption=f"{caption_has_spoiler}{title}{caption_has_spoiler}"))
            except:
                pass

    elif types == 'vid':
        channels = ["sssnnnc"]
        channel = random.choice(channels)
        count = await client.search_messages_count(chat_id=channel, filter=enums.MessagesFilter.VIDEO)
        random_offset = random.randint(1, count)
        async for m in client.search_messages(chat_id=channel, offset=random_offset, limit=1, filter=enums.MessagesFilter.VIDEO):
            await client.send_video(chat_id, m.video.file_id, has_spoiler=True)

    elif types == 'mjx':
        r = requests.get("https://mjx.0o0o0o0.workers.dev/", stream=True)
        if r.ok:
            url = r.json()['url']
            caption = r.json()['des']
            await client.send_message(chat_id, f'{caption_has_spoiler}\n[买家秀：]({url})\n__{caption}__{caption_has_spoiler}', disable_web_page_preview=False)
        else:
            await client.send_message(chat_id, '获取失败~')
