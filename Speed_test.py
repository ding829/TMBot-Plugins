from client.utils import OnCmd
from client.config import prefix, TMPDIR
import math
import platform
import requests
import subprocess
import json
import os
import tarfile

def convert_size(b, suffix="B", factor=1024):
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f'{b:.2f}{unit}{suffix}'
        b /= factor

def is_json(content):
    try:
        json.loads(content)
    except:
        return False
    return True

def is_number(s):
    try:
        float(s)
        return True
    except:
        pass
    try:
        import unicodedata
        for i in s:
            unicodedata.numeric(i)
        return True
    except:
        pass
    return False

longHelp = f"""使用示例：
1、默认测速：`{prefix}speedtest`
2、获取服务器：`{prefix}speedtest L`
3、指定服务器：`{prefix}speedtest <服务器 id>`
"""

PIP = "requests"

@OnCmd("Speedtest", help="speedtest 测速", doc=longHelp)
async def handler(client, msg, chat_id, args, reply):
    await msg.edit(f'运行中...')
    speedtest = f'{TMPDIR}/speedtest'
    arg = args[0] if len(args) >= 1 else None
    async def sptest():
        await msg.edit(f'测速中...')
        cmd = [speedtest, "--format=json-pretty", "--progress=no", "--accept-license", "--accept-gdpr"]
        if is_number(arg):
            cmd.append(f"--server-id={arg}")
        try:
            output = subprocess.check_output(cmd)
        except Exception as e:
            output = e
        return output

    if not os.path.exists(speedtest):
        await msg.edit("下载 speedtest 中...")
        arch = platform.machine()
        url = f'https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-{arch}.tgz'
        try:
            req = requests.get(url)
            if req.ok:
                with open(f'{speedtest}.tgz', "wb") as f:
                    f.write(req.content)
                tar = tarfile.open(f'{speedtest}.tgz', "r:*")
                tar.extract("speedtest", path=TMPDIR)
        except:
            await msg.edit("下载 speedtest 失败~")

    if os.path.exists(speedtest):
        if arg == 'L':
            await msg.edit(f'获取服务器中...')
            cmd = [speedtest, "-L", "--format=json-pretty", "--accept-license", "--accept-gdpr"]
            try:
                output = subprocess.check_output(cmd)
            except Exception as e:
                await msg.edit(f'获取服务器失败...')
            else:
                content = "**SPEEDTEST 服务器列表**\n\n"
                servers = json.loads(output)["servers"]
                for s in servers:
                    content += f"▪️ `{s['id']}`： `{s['name']} - {s['location']} {s['country']}`\n"
                await msg.edit(content)
        else:
            output = await sptest()
            if is_json(output):
                await msg.delete()
                data = json.loads(output)
                content = "**SPEEDTEST**\n\n"
                content += f'下载：`{convert_size(data["download"]["bandwidth"], suffix="B/s")} - {convert_size(data["download"]["bytes"], suffix="B", factor=1000)}`\n'
                content += f'上传：`{convert_size(data["upload"]["bandwidth"], suffix="B/s")} - {convert_size(data["upload"]["bytes"], suffix="B", factor=1000)}`\n'
                content += f'Ping：`{data["ping"]["latency"]}ms - {data["ping"]["jitter"]}`\n'
                content += f'客户端：`{data["isp"]}`\n'
                content += f'服务器：`{data["server"]["name"]} - {data["server"]["location"]} {data["server"]["country"]}`\n'
                await client.send_photo(chat_id, photo=f'{data["result"]["url"]}.png', caption=content)
            else:
                await msg.edit(f'测速失败...')
