#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import configparser
import subprocess
import time
import os
import codecs
from rcon.battleye import Client

# 读取配置文件
config = configparser.ConfigParser()
with codecs.open('config.ini', 'r', encoding='utf-8-sig') as f:
    config.read_file(f)
program_path = config.get('Settings', 'program_path')
rcon_enabled = config.getboolean('RCON', 'rcon_enabled')

restart_interval_hours = config.get('Settings', 'restart_interval_hours')

shutdown_notices = dict(item.split(':') for item in config.get('Settings', 'shutdown_notices').split(';'))

restart_interval = float(restart_interval_hours) * 3600
appName = 'PalServer-Win64-Test-Cmd.exe'


# 轮询任务(固定延迟执行)
def polling_task():
    """
    基本逻辑
    关闭运行的palserver服务 → 启动服务 → 等待服务重启→
    倒计时还剩30秒打开rcon.exe发送 Broadcastt 服务器关服倒计时30s → 每10秒发送一次 Broadcastt 直到倒计时结束
    """
    while True:

        print("正在关闭任何在运行的palserver服务......")
        subprocess.run(['taskkill', '/f', '/im', appName], stderr=subprocess.DEVNULL)

        # 启动程序
        print("正在启动程序......")
        subprocess.Popen([program_path])

        # 服务器持续运行时间(重启间隔)
        for i in range(int(restart_interval), 0, -1):

            # 还剩30秒的时候发送rcon关服消息提醒
            if str(i) in shutdown_notices and rcon_enabled:  # 检查是否有对应的通知
                print("\n正在打开rcon.exe......")
                os.chdir(rcon_path)
                # 启动rcon.exe并发送命令
                rcon_process = subprocess.Popen(['rcon.exe'], stdin=subprocess.PIPE)
                rcon_process.stdin.write((shutdown_notices[str(i)] + '\n').encode())
                rcon_process.stdin.flush()  # 确保消息被发送
                rcon_process.stdin.close()

            print(f'\r服务器将在 {i} 秒后重启......', end='')
            time.sleep(1)


if __name__ == '__main__':
    polling_task()
