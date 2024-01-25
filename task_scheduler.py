#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import subprocess
import time
import psutil
import multiprocessing
import read_conf
from utils.log_control import INFO, ERROR, WARNING
from rcon.source import Client
from rcon.source.proto import Packet


class TaskScheduler:
    def __init__(self):
        self.conf = read_conf.read_config()
        self.appName = 'PalServer-Win64-Test-Cmd.exe'
        self.host = self.conf['rcon_host'],
        self.port = self.conf['rcon_port'],
        self.passwd = self.conf['rcon_password'],
        self.rcon_command = self.conf['rcon_command']

    # 修改rcon源代码，忽略SessionTimeout异常
    def patched_run(self, command: str, *args: str, encoding: str = "utf-8") -> str:
        """Patched run method that ignores SessionTimeout exceptions."""
        request = Packet.make_command(command, *args, encoding=encoding)
        response = self.communicate(request)

        # Ignore SessionTimeout exceptions
        # if response.id != request.id:
        #     raise SessionTimeout()

        return response.payload.decode(encoding)

    # Apply the monkey patch
    Client.run = patched_run

    # 轮询任务(固定延迟执行)
    def polling_task(self):

        while True:
            INFO.logger.info("正在关闭任何在运行的palserver服务......")
            print("正在关闭任何在运行的palserver服务......")
            subprocess.run(['taskkill', '/f', '/im', self.appName], stderr=subprocess.DEVNULL)

            # 启动程序
            INFO.logger.info("正在启动程序......")
            print("正在启动程序......")
            program_args = [self.conf['program_path']]
            if self.conf['use_multicore_options']:
                INFO.logger.info("已开启多核选项")
                print("已开启多核选项")
                program_args.extend(["-useperfthreads", "-NoAsyncLoadingThread", "-UseMultithreadForDS"])
            subprocess.Popen(program_args)

            INFO.logger.info(f'服务器将进入重启倒计时，设置时长为 {self.conf["restart_interval"]} 秒......')
            print(f'服务器将进入重启倒计时，设置时长为 {self.conf["restart_interval"]} 秒......')
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
                if str(i) in self.conf['shutdown_notices'] and self.conf['rcon_enabled']:  # 检查是否有对应的通知
                    if self.conf['rcon_command']:
                        INFO.logger.info("RCON指令 {0}，正在发送关服通知......".format(self.conf['rcon_command']))
                        print("RCON指令 {0}，正在发送关服通知......".format(self.conf['rcon_command']))
                        with Client(
                                host=self.conf['rcon_host'],
                                port=self.conf['rcon_port'],
                                passwd=self.conf['rcon_password'],
                                timeout=1) as client:
                            message = self.conf['shutdown_notices'][str(i)]
                            response = client.run(f"{self.conf['rcon_command']} {message}", 'utf-8')
                            INFO.logger.info('Response:{0}'.format(response))
                            print('Response:', response)
                print(f'\r服务器将在 {i} 秒后重启......', end='')
                time.sleep(1)

    # 守护进程
    def daemon_task(self):
        while True:
            try:
                # 检查程序是否正在运行
                is_running = any([p.info['name'] == self.appName for p in psutil.process_iter(['name'])])

                if not is_running:
                    # 启动程序
                    INFO.logger.info("守护进程正在启动程序......")
                    print("守护进程正在启动程序......")
                    time.sleep(1)
                    program_args = [self.conf['program_path']]
                    if self.conf['use_multicore_options']:
                        program_args.extend(["-useperfthreads", "-NoAsyncLoadingThread", "-UseMultithreadForDS"])
                    subprocess.Popen(program_args)
                time.sleep(int(self.conf['daemon_time']))

            # 只有异常退出才会触发，手动关闭进程不会触发
            except Exception as e:
                ERROR.logger.error(f"程序异常终止，错误信息：{e}\n正在尝试重启程序......")
                print(f"程序异常终止，错误信息：{e}\n正在尝试重启程序......")
                continue


if __name__ == '__main__':
    Task = TaskScheduler()
    daemon_enabled = Task.conf['daemon_enabled']
    if daemon_enabled:
        print("守护进程已启动,每隔{0}秒检测PalServer进程......".format(Task.conf['daemon_time']))
        daemon_process = multiprocessing.Process(target=Task.daemon_task)
        daemon_process.start()
        daemon_process.join()
    else:
        print("轮询任务已启动,每隔{0}秒重启PalServer进程......".format(Task.conf['restart_interval']))
        Task.polling_task()
