from client.utils import OnCmd
from googlesearch import search
from urllib import parse

PIP="googlesearch-python"

@OnCmd("google", help="谷歌搜索")
async def handler(client, msg, chat_id, args, reply):
    title = None
    result = {}
    if len(args) >= 1:
        query = ' '.join(args)
    elif reply:
        query = msg.reply_to_message.text if msg.reply_to_message.text else msg.reply_to_message.caption
    else:
        await msg.edit("请加入搜索内容~")

    if query:
        await msg.edit(f"正在搜索...\n\n{query}")
        for i in search(query, advanced=True):
            result[i.title] = i.url
            if len(result) > 10:
                break
        if result:
            links = '\n\n'.join(f"{i+1}、 [{item[0]}]({item[1]})" for i, item in enumerate(result.items()))
            content = f"🔎 | **Google** | [{query}](https://www.google.com/search?q={parse.quote(query)})\n\n{links}"
            await msg.edit(text=content, disable_web_page_preview=True)
        else:
            await msg.edit(f"搜索失败~\n建议手动搜索：[{query}](https://www.google.com/search?q={parse.quote(query)})")
