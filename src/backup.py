#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import shutil
import time
import datetime
import os
from src import read_conf
from src.utils.log_control import INFO


class Backup:

    def __init__(self):
        self.conf = read_conf.read_config()
        self.appName = 'PalServer-Win64-Test-Cmd.exe'
        self.backup_source = os.path.join(self.conf['main_directory'], 'Pal', 'Saved')

    # 备份任务
    def backup_task(self):
        # 在当前目录下创建名为Backup的文件夹
        if self.conf['backup_dir'] == '':
            backup_dir = 'Backup'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
        else:
            backup_dir = self.conf['backup_dir']
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

        # 如果备份间隔不为空，则执行备份
        if self.conf['backup_interval']:

            INFO.logger.info("自动备份已开启，正在进行备份......")
            print("\n自动备份已开启，正在进行备份......")
            try:
                while True:
                    datetime_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

                    # 备份文件
                    shutil.copytree(self.backup_source, os.path.join(backup_dir, f"Saved_{datetime_now}"))

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
            except FileNotFoundError as e:
                INFO.logger.error(f"备份失败，{e}")
                print(f"备份失败，{e}")

        # 备份时间必须大于等于60秒
        elif int(self.conf['backup_interval']) < 60:
            INFO.logger.error("备份时间 backup_interval 必须大于等于1分钟，请重新设置！")
            print("备份时间 backup_interval 备份时间必须大于等于1分钟，请重新设置！")
            time.sleep(3)
            exit(0)

        # 如果为空，则不执行备份
        else:
            INFO.logger.info("自动备份已关闭，不执行备份任务！")
            print("自动备份已关闭，不执行备份任务！")


if __name__ == '__main__':
    backup = Backup()
    backup.backup_task()
