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
        # backup_dir为空时，设置当前目录下的Backup文件夹为备份目录
        if self.conf['backup_dir'] == '':
            backup_dir = os.path.join(os.getcwd(), 'Backup')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            self.conf['backup_dir'] = backup_dir
        else:
            # 使用配置文件中的备份目录
            backup_dir = self.conf['backup_dir']
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

        # 如果备份间隔不为空，则执行备份
        if self.conf['backup_interval']:

            INFO.logger.info("自动备份已开启，正在进行备份......")
            print("\n自动备份已开启，正在进行备份......")

            while True:
                datetime_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

                # 备份文件
                shutil.copytree(self.backup_source, os.path.join(backup_dir, f"Saved_{datetime_now}"))

                time.sleep(1)
                INFO.logger.info("备份成功，文件名为：Saved_" + datetime_now)
                print("\r备份成功，文件名为：Saved_" + datetime_now)
                # 存档备份位置
                backup_path = os.path.join(os.getcwd(), backup_dir)
                print(f"\r存档备份位置：{backup_path}")
                # 在备份执行前删除旧的备份
                self.delete_old_backups(int(self.conf['del_old_backup_days']))
                # 显示倒计时并等待指定的备份间隔
                for i in range(int(self.conf['backup_interval']), 0, -1):
                    print(f'\r下一次备份将在 {i} 秒后开始...', end='')
                    time.sleep(1)

        # 备份时间必须大于等于60秒
        elif int(self.conf['backup_interval']) < 60:
            INFO.logger.error("备份时间 backup_interval 必须大于等于1分钟，请重新设置！")
            print("\r备份时间 backup_interval 备份时间必须大于等于1分钟，请重新设置！")
            time.sleep(3)
            exit(0)

        # 如果为空，则不执行备份
        else:
            INFO.logger.info("自动备份已关闭，不执行备份任务！")
            print("\r自动备份已关闭，不执行备份任务！")

    def delete_old_backups(self, days):
        """
        删除指定天数之前的备份文件
        :param days: 指定的天数
        """
        if self.conf['del_old_backup_days']:
            INFO.logger.info(f"已开启删除备份文件，每隔{self.conf['backup_interval']}秒执行一次")
            print(f"\n已开启删除备份文件，每隔{self.conf['backup_interval']}秒执行一次")
            cutoff = datetime.datetime.now() - datetime.timedelta(days=days)

            files = os.listdir(self.conf['backup_dir'])

            for file in files:
                file_path = os.path.join(self.conf['backup_dir'], file)
                # 检查文件是否是一个备份文件，可以根据你的需要修改这个条件
                if os.path.isdir(file_path) and 'Saved_' in file:
                    # 从文件名解析日期和时间
                    date_str = file.split('_')[1]  # 获取日期字符串
                    time_str = file.split('_')[2]  # 获取时间字符串
                    file_datetime = datetime.datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H-%M-%S')

                    # 如果文件的创建时间早于cutoff，删除文件
                    if file_datetime < cutoff:
                        try:
                            shutil.rmtree(file_path)  # 删除目录
                            INFO.logger.info(f"开始删除旧的备份文件，已成功删除备份文件：{file}")
                            print(f"开始删除旧的备份文件，已成功删除备份文件：{file}")
                        except OSError as e:
                            INFO.logger.error(f"删除备份文件失败：{file}, 原因：{e}")
                            print(f"删除备份文件失败：{file}, 原因：{e}")
        else:
            INFO.logger.info("未设置备份文件的自动删除天数，不执行删除任务！")
            print("未设置备份文件的自动删除天数，不执行删除任务！")


if __name__ == '__main__':
    backup = Backup()
    backup.backup_task()

