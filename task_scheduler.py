#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import configparser
import shutil
import subprocess
import time
import datetime
import os

# 创建一个配置文件解析器
config = configparser.ConfigParser()

# 读取配置文件
read_data = config.read('config.ini', encoding='utf-8')
task_type = config.get('Settings', 'task_type')
program_path = config.get('Settings', 'program_path')

rcon_path = config.get('Settings', 'rcon_path')
restart_interval_hours = config.get('Settings', 'restart_interval_hours')


restart_interval = int(restart_interval_hours) * 3600
datetime_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
appName = 'PalServer-Win64-Test-Cmd.exe'


# 轮询任务(固定延迟执行)
def polling_task():
    """
    基本逻辑
    关闭运行的palserver服务 → 启动服务 → 等待服务重启→
    倒计时还剩10秒打开rcon.exe发送 Broadcastt 服务器关服倒计时10s →
    等待10秒 → 关闭rcon.exe → ......
    """
    while True:
        # 结束当前正在运行的程序，忽略错误信息
        print("正在关闭任何在运行的palserver服务......")
        task_exists = subprocess.run(['tasklist', '/NH', '/FI', f'IMAGENAME eq {appName}*'], stdout=subprocess.PIPE,
                                     text=True)
        if appName in task_exists.stdout:
            # 结束当前正在运行的程序，忽略错误信息
            subprocess.run(['taskkill', '/f', '/im', appName], stderr=subprocess.DEVNULL)

        # 启动程序
        print("正在启动程序......")
        subprocess.Popen([program_path])

        # 服务器持续运行时间(重启间隔)
        for i in range(restart_interval, 10, -1):
            print(f'\r服务器将在 {i} 秒后重启......', end='')
            time.sleep(1)

        # 还剩10秒的时候自动进入rcon-0.10.3-win64目录
        os.chdir(rcon_path)

        # 在rcon-0.10.3-win64目录中启动rcon.exe并发送命令
        rcon_process = subprocess.Popen(['rcon.exe'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 显示倒计时并等待剩余的10秒
        for i in range(10, 0, -1):
            rcon_process.stdin.write(f'Broadcast The_server_is_about_to_restart_with_a_countdown_of_{i}_seconds.\n'.encode())
            rcon_process.stdin.flush()  # 确保消息被发送
            time.sleep(1)


# 计划任务(每天特定时间执行)
def scheduled_task():

    # 结束当前正在运行的程序，忽略错误信息
    print("正在关闭任何在运行的palserver服务......")
    task_exists = subprocess.run(['tasklist', '/NH', '/FI', f'IMAGENAME eq {appName}*'], stdout=subprocess.PIPE,
                                 text=True)
    if appName in task_exists.stdout:
        # 结束当前正在运行的程序，忽略错误信息
        subprocess.run(['taskkill', '/f', '/im', appName], stderr=subprocess.DEVNULL)

    # 启动程序
    print("正在启动程序......")
    subprocess.Popen([program_path])

    # 对于每个计划任务，如果设置的时间不为空，则创建计划任务
    for i in range(1, 4):
        task_name = f'PalServerRestart{i}'
        start_time = config.get('Settings', f'start_time_{i}')
        if start_time:
            # 删除已有的任务
            subprocess.run(['schtasks', '/Delete', '/TN', task_name, '/F'], stderr=subprocess.DEVNULL)
            print("当天计划任务已清空")
            # 创建新任务
            subprocess.run(['schtasks', '/Create', '/SC', 'DAILY', '/TN', task_name, '/TR',
                            os.path.realpath(__file__), '/ST', start_time])
            print(f"新计划任务'{task_name}'创建成功，每天将在{start_time}重启服务器")


# 轮询任务
if task_type == '1':
    print("当前进行的是轮询任务，已读取config配置")
    polling_task()
# 计划任务
elif task_type == '2':
    print("当前进行的是计划任务，已读取config配置")
    scheduled_task()
else:
    print(
        f"配置 config.ini 中的任务类型配置项 '{task_type}'无效")
