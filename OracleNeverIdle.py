from client.utils import OnScheduler

import sys
import time
import math
import threading
import asyncio
from psutil import virtual_memory, cpu_percent

PIP = "psutil"

@OnScheduler(cron="* * * * *", help="甲骨文保活", doc='占用 10% 的 cpu 和内存')
async def handler():
    async def occupy():
        # https://stackoverflow.com/a/24016138
        cpu_time_utilisation = float(15)/100
        on_time = 0.1 * cpu_time_utilisation
        off_time = 0.1 * (1-cpu_time_utilisation)
        cpu = cpu_percent(3) < 10

        m = virtual_memory().total * 0.10
        mem = virtual_memory().used < m

        if cpu or mem:
            while True:
                if cpu:
                    start_time = time.process_time()
                    while time.process_time() - start_time < on_time:
                        math.factorial(100)
                    time.sleep(off_time)
                if virtual_memory().used < m:
                    xxx = ' ' * int(m)

    def async_func():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(occupy())
        loop.close()

    thread = threading.Thread(target=async_func)
    thread.daemon = True
    thread.start()
