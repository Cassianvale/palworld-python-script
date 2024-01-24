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

read_data = config.read('config.ini', encoding='utf-8')

backup_source = config.get('Settings', 'backup_source')
backup_target = config.get('Settings', 'backup_target')
backup_interval_hours = config.get('Settings', 'backup_interval_hours')
rcon_path = config.get('Settings', 'rcon_path')
datetime_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


# 备份任务
def backup_task():

    # 如果备份间隔不为空，则执行备份
    if backup_interval_hours:
        backup_interval = int(backup_interval_hours) * 3600  # 将备份间隔转换为秒

        while True:
            # 备份文件
            print("自动备份已开启，正在进行备份......")
            shutil.copytree(backup_source, os.path.join(backup_target, f"Saved_{datetime_now}"))
            time.sleep(1)
            print("备份成功，文件名为：Saved_" + datetime_now)

            # 显示倒计时并等待指定的备份间隔
            for i in range(backup_interval, 0, -1):
                print(f'\r下一次备份将在 {i} 秒后开始...', end='')
                time.sleep(1)
    else:
        print("自动备份未开启，需要自动备份请需改config.ini配置")


if __name__ == '__main__':
    backup_task()
