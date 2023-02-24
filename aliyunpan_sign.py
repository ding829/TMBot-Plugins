from pyrogram import Client
from config import prefixes, command, GlobalSN, Packages, data_dir

import os
import json

if Packages('requests'):
    import requests

config = f"{data_dir}/aliyunpan_sign.json"
if not os.path.exists(config):
    with open(config,"w", encoding='utf-8') as f:
        json.dump({"token": ""}, f, indent=4, ensure_ascii=False)

doc = f"""
1、网页登录阿里云盘官网 `https://www.aliyundrive.com/drive`
2、按 `F12`，进入开发者工具模式，在顶上菜单栏点 `Application` ，然后在左边菜单找到 `Local storage` 下面的 `https://www.aliyundrive.com` 这个域名，点到这个域名会看到有一个 `token` 选项，再点 `token` ，就找到 `refresh_token` 了
3、设置 token：`{prefixes}alips set token`，请勿在公共群设置。

此插件源自[aliyunpan-sign](https://www.bboy.app/2023/02/20/%E5%86%99%E4%BA%86%E4%B8%80%E4%B8%AA%E9%98%BF%E9%87%8C%E4%BA%91%E7%9B%98%E8%87%AA%E5%8A%A8%E7%AD%BE%E5%88%B0%E8%84%9A%E6%9C%AC/)
"""

@Client.on_message(command('alips'), group=GlobalSN.reg(locals(), 'cmd', 'alips', '阿里云盘签到', doc))
async def handler(client, message):
    args = message.text.strip().split()

    if len(args) > 2 and args[1] == 'set':
        with open(config,"w", encoding='utf-8') as f:
            conf = {"token": args[2]}
            json.dump(conf, f, indent=4, ensure_ascii=False)
        await message.edit(f'设置成功，发送 `{prefixes}alips` 进行签到~')
        return

    with open(config,"r") as f:
        conf = json.load(f)
    token = conf["token"]

    if not token:
        await message.edit(f'请先设置 token，发送 `{prefixes}help alips` 获取帮助~')
        return

    def aliyundrive_sign(token):
        update_token_url = "https://auth.aliyundrive.com/v2/account/token"
        signin_url = "https://member.aliyundrive.com/v1/activity/sign_in_list"

        headers = {
            'Content-Type': 'application/json'
        }
        data = json.dumps({
            'grant_type': 'refresh_token',
            'refresh_token': token
        })
        req = requests.Session()
        resp = req.post(update_token_url, data=data, headers=headers).text
        access_token = json.loads(resp)['access_token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        resp = req.post(signin_url, data=data, headers=headers)
        result = json.loads(resp.text)
        return result

    result = aliyundrive_sign(token)

    if not result:
        await message.edit("签到失败!")
        return

    if not result['success']:
        await message.edit("签到失败!")
        return

    content = "签到成功!\n"
    pic = None
    for i in reversed(result['result']['signInLogs']):
        if i['isReward'] and i['reward']:
            content += f"获得 {i['reward']['name']}{i['reward']['description']}！" if i['reward']['name'] else "ㅤ"
            pic = i['reward']['background']
            break
    if pic:
        await message.delete()
        await message.reply_photo(pic, caption=content, quote=False)
    else:
        await message.edit(content)
