#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import shutil
import time
import datetime
import os
import read_conf
from utils.log_control import INFO, ERROR, WARNING


class Backup:

    def __init__(self):
        self.conf = read_conf.read_config()
        self.appName = 'PalServer-Win64-Test-Cmd.exe'

    # 备份任务
    def backup_task(self):
        # 在当前目录下创建名为Backup的文件夹
        backup_dir = 'Backup'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # 如果备份间隔不为空，则执行备份
        if self.conf['backup_interval']:

            INFO.logger.info("自动备份已开启，正在进行备份......")
            print("\n自动备份已开启，正在进行备份......")

            while True:
                datetime_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

                # 备份文件
                shutil.copytree(self.conf['backup_source'], os.path.join(backup_dir, f"Saved_{datetime_now}"))

                time.sleep(1)
                INFO.logger.info("备份成功，文件名为：Saved_" + datetime_now)
                print("备份成功，文件名为：Saved_" + datetime_now)
                # 存档备份位置
                backup_path = os.path.join(os.getcwd(), backup_dir)
                print(f"存档备份位置：{backup_path}")
                # 显示倒计时并等待指定的备份间隔
                for i in range(int(self.conf['backup_interval']), 0, -1):
                    print(f'\r下一次备份将在 {i} 秒后开始...', end='')
                    time.sleep(1)

        else:
            INFO.logger.info("自动备份未开启，需要自动备份请需改config.ini配置")
            print("自动备份未开启，需要自动备份请需改config.ini配置")


if __name__ == '__main__':
    backup = Backup()
    backup.backup_task()
