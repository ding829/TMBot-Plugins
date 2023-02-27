from pyrogram import Client, enums
from config import command, GlobalSN, data_dir, prefixes

import time
import json
import aiohttp
import os

config = f"{data_dir}/bwh.json"
if not os.path.exists(config):
    with open(config,"w", encoding='utf-8') as f:
        conf = {"VEID": "", "API_KEY": ""}
        json.dump(conf, f, indent=4, ensure_ascii=False)

@Client.on_message(command('bwh'), group=GlobalSN.reg(locals(), 'cmd', 'bwh', '获取搬瓦工 vps 信息', f'在搬瓦工后台获取 api 填入配置文件 `{config}` 中', '0.1'))
async def handler(client, message):
    await message.edit("获取中...")
    content = str()
    conf = str()
    with open(config,"r") as f:
        conf = json.load(f)
    VEID = conf["VEID"]
    API_KEY = conf["API_KEY"]
    if bool(API_KEY and VEID):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.64clouds.com/v1/getLiveServiceInfo?veid={VEID}&api_key={API_KEY}') as resp:
                if resp.status == 200:
                    LiveServiceInfo = json.loads(await resp.text())
                    if LiveServiceInfo["error"] == 0:
                        node_datacenter = LiveServiceInfo['node_datacenter']
                        ve_status = LiveServiceInfo['ve_status']
                        load_average = LiveServiceInfo['load_average']
                        mem_available = str(LiveServiceInfo['mem_available_kb'] / 1000)
                        plan_ram = str(LiveServiceInfo['plan_ram'] / 1024 / 1024)
                        ve_used_disk_space = str(round(LiveServiceInfo['ve_used_disk_space_b'] / 1024 / 1024 / 1024,2))
                        ve_disk_quota_gb = LiveServiceInfo['ve_disk_quota_gb']
                        monthly_data_multiplier = LiveServiceInfo['monthly_data_multiplier']
                        data_counter = str(round(LiveServiceInfo['data_counter'] * monthly_data_multiplier / 1024 / 1024 / 1024,2))
                        plan_monthly_data = str(round(LiveServiceInfo['plan_monthly_data'] / 1024 / 1024 / 1024,2))
                        data_next_reset = time.strftime("%Y-%m-%d", time.localtime(LiveServiceInfo['data_next_reset']))

                        content = f'**{node_datacenter}**\n\n'
                        content += f'状态：`{ve_status},{load_average}`\n'
                        content += f'内存（可用）：`{mem_available}/{plan_ram}MB`\n'
                        content += f'硬盘（已用）：`{ve_used_disk_space}/{ve_disk_quota_gb}GB`\n'
                        content += f'流量（已用）：`{data_counter}/{plan_monthly_data}GB`\n'
                        content += f'流量重置日期：`{data_next_reset}`\n'
    else:
        content = f"没有获取到相关 API 值，请发送 `{prefixes}hep bwh` 获取帮助~"  
    await message.edit(content)
