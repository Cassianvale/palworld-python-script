#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import subprocess
import time
import os
import codecs
import psutil
import multiprocessing
import read_conf


class TaskScheduler:
    def __init__(self):
        self.conf = read_conf.read_config()
        self.appName = 'PalServer-Win64-Test-Cmd.exe'

    # 轮询任务(固定延迟执行)
    def polling_task(self):
        """
        基本逻辑
        关闭运行的palserver服务 → 启动服务 → 等待服务重启→
        倒计时还剩30秒打开rcon.exe发送 Broadcastt 服务器关服倒计时30s → 每10秒发送一次 Broadcastt 直到倒计时结束
        """
        while True:

            print("正在关闭任何在运行的palserver服务......")
            subprocess.run(['taskkill', '/f', '/im', self.appName], stderr=subprocess.DEVNULL)

            # 启动程序
            print("正在启动程序......")
            program_args = [self.conf['program_path']]
            if self.conf['use_multicore_options']:
                program_args.extend(["-useperfthreads", "-NoAsyncLoadingThread", "-UseMultithreadForDS"])
            subprocess.Popen(program_args)

            # 服务器持续运行时间(重启间隔)
            for i in range(int(self.conf['restart_interval']), 0, -1):
                # 如果设置了检查内存使用情况memory_monitor_enabled
                if self.conf['memory_monitor_enabled']:
                    # 检查内存使用情况
                    mem_info = psutil.virtual_memory()
                    mem_usage = mem_info.percent  # 获取内存使用百分比

                    # 如果内存使用超过阈值，则跳出倒计时，进行重启操作
                    if mem_usage > self.conf['memory_usage_threshold']:
                        print(f"内存使用超过{self.conf['memory_usage_threshold']}%，正在重启程序......")
                        break

                # 还剩30秒的时候发送rcon关服消息提醒
                if str(i) in self.conf['shutdown_notices'] and self.conf['conf.rcon_enabled']:  # 检查是否有对应的通知
                    print("\n正在打开rcon......")

                    # 启动rcon.exe并发送命令
                    rcon_process = subprocess.Popen(['rcon.exe'], stdin=subprocess.PIPE)
                    rcon_process.stdin.write((self.conf['shutdown_notices'][str(i)] + '\n').encode())
                    rcon_process.stdin.flush()  # 确保消息被发送
                    rcon_process.stdin.close()

                print(f'\r服务器将在 {i} 秒后重启......', end='')
                time.sleep(1)

    # 守护进程
    def daemon_task(self):
        while True:
            # 检查程序是否正在运行
            is_running = any([p.info['name'] == self.conf['appName'] for p in psutil.process_iter(['name'])])

            if not is_running:
                try:
                    # 启动程序
                    print("正在启动程序......")
                    time.sleep(1)
                    program_args = [self.conf['program_path']]
                    if self.conf['use_multicore_options']:
                        program_args.extend(["-useperfthreads", "-NoAsyncLoadingThread", "-UseMultithreadForDS"])
                    subprocess.Popen(program_args)
                except Exception as e:
                    print(f"程序启动失败，错误信息：{e}")
            time.sleep(int(self.conf['daemon_time']))


if __name__ == '__main__':
    Task = TaskScheduler()
    daemon_enabled = Task.conf['daemon_enabled']
    if daemon_enabled:
        daemon_process = multiprocessing.Process(target=Task.conf['daemon_task'])
        daemon_process.start()
        daemon_process.join()
    else:
        Task.polling_task()
