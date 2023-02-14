from client.utils import OnCmd
from client.config import prefix
import requests
from urllib import parse

PIP = "requests"

doc=f'默认输出前 15 条热搜，若要输出全部请加 `more`，如：`{prefix}weibo more`'

@OnCmd("weibo", help="获取微博热搜", doc=doc)
async def handler(client, msg, chat_id, args, reply):
    arg = args[0] if len(args) > 0 else None
    url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&show_cache_when_error=1&extparam=seat%3D1%26lcate%3D1001%26filter_type%3Drealtimehot%26c_type%3D30%26dgr%3D0%26region_relas_conf%3D0%26cate%3D10103%26mi_cid%3D100103%26pos%3D0_0%26display_time%3D1673475482%26pre_seqid%3D1539928376&luicode=10000011&lfid=231583"
    await msg.edit("获取微博热搜中...")
    r = requests.get(url, stream=True)
    if r.ok:
        content = r.json()["data"]["cards"][0]["card_group"]
        del content[0]
        text = f'📰ㅤ**微博热搜**\n\n'
        N = 1
        for i in range(len(content)):
            if len(text) > 9500:
                break
            if arg != "more" and i > 15:
                break
            if "promotion" not in content[i]:
                text += f'{N}、[{content[i]["desc"]}](https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{parse.quote(content[i]["desc"])})\n'
                N = N + 1
        await msg.edit(text, disable_web_page_preview=True)
    else:
        await msg.edit("获取失败！")