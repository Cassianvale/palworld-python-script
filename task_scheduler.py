#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import configparser
import subprocess
import time
import os
import psutil

# 创建一个配置文件解析器
config = configparser.ConfigParser()

# 读取配置文件
read_data = config.read('config.ini', encoding='utf-8')
# task_type = config.get('Settings', 'task_type')
program_path = config.get('Settings', 'program_path')

rcon_path = config.get('Settings', 'rcon_path')
restart_interval_hours = config.get('Settings', 'restart_interval_hours')

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
            print(f'\r服务器将在 {i} 秒后重启......', end='')
            time.sleep(1)
            # 还剩30秒的时候发送rcon关服消息提醒
            if i <= 30 and i % 10 == 0:
                print("\n正在打开rcon.exe......")
                os.chdir(rcon_path)
                # 启动rcon.exe并发送命令
                rcon_process = subprocess.Popen(['rcon.exe'], stdin=subprocess.PIPE)
                rcon_process.stdin.write(
                    f'Broadcast The_server_is_about_to_restart_with_a_countdown_of_{i}_seconds.\n'.encode())
                rcon_process.stdin.flush()  # 确保消息被发送
                rcon_process.stdin.close()


# def scheduled_task():
#
#     # 删除没有后缀数字的任务
#     subprocess.run(['schtasks', '/Delete', '/TN', 'PalServerRestart', '/F'], stderr=subprocess.DEVNULL)
#     subprocess.run(['schtasks', '/Delete', '/TN', 'PalServerRestart1', '/F'], stderr=subprocess.DEVNULL)
#     subprocess.run(['schtasks', '/Delete', '/TN', 'PalServerRestart2', '/F'], stderr=subprocess.DEVNULL)
#     subprocess.run(['schtasks', '/Delete', '/TN', 'PalServerRestart3', '/F'], stderr=subprocess.DEVNULL)
#
#     print("正在关闭任何在运行的palserver服务......")
#     subprocess.run(['taskkill', '/f', '/im', appName], stderr=subprocess.DEVNULL)
#
#     # 启动程序
#     print("正在启动程序......")
#     subprocess.Popen([program_path])
#
#     # 对于每个计划任务，如果设置的时间不为空，则创建计划任务
#     for i in range(1, 4):
#         task_name = f'PalServerRestart{i}'
#         start_time = config.get('Settings', f'start_time_{i}')
#
#         if start_time:
#             # 创建新任务
#             subprocess.run(
#                 ['SCHTASKS', '/Create', '/SC', 'DAILY', '/TN', task_name, '/TR', f'{program_path}', '/ST', start_time])
#             print(f"新计划任务'{task_name}'创建成功，每天将在{start_time}重启服务器")
#
#     # 无限循环，保持终端窗口开启
#     while True:
#         time.sleep(1)

#
# # 轮询任务
# if task_type == '1':
#     print("当前运行的是轮询任务，已读取config配置")
#     polling_task()
# # 计划任务
# elif task_type == '2':
#     print("当前运行的是计划任务，已读取config配置")
#     scheduled_task()
# else:
#     print(
#         f"配置 config.ini 中的任务类型配置项 'task_type = {task_type}'无效")

if __name__ == '__main__':
    polling_task()
