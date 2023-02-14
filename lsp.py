from client.utils import OnDraft
from pyrogram import enums
from pyrogram.types import InputMediaPhoto
import random, asyncio, re, requests

PIP = "requests"

@OnDraft("lsp", help="来点色图")
async def handler(client, update, chat_id, args, reply):

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
        mesg = await client.send_photo(chat_id, photos[0], has_spoiler=True, caption=f"||[{title}||", reply_to_message_id=reply)
        del photos[0]
        try:
            for i, photo in enumerate(photos):
                if i < len(photos):
                    await asyncio.sleep(5)
                    await client.edit_message_media(chat_id, mesg.id, InputMediaPhoto(photo, has_spoiler=True, caption=f"||[{title}||"))
        except:
            pass
