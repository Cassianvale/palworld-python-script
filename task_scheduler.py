#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import subprocess
import time
import psutil
import read_conf
from utils.log_control import INFO
from rcon.source import Client
from rcon.source.proto import Packet
import threading


class TaskScheduler:
    def __init__(self):
        self.conf = read_conf.read_config()
        self.appName = 'PalServer-Win64-Test-Cmd.exe'
        self.host = self.conf['rcon_host'],
        self.port = self.conf['rcon_port'],
        self.passwd = self.conf['rcon_password'],
        self.rcon_command = self.conf['rcon_command']
        self.daemon_time  = self.conf['daemon_time']
        self.arguments = self.conf.get('arguments', '').split()

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
            if self.conf['restart_interval'] < 60:
                INFO.logger.error("[ 轮询任务 ] 服务器重启时间 restart_interval 必须大于等于1分钟，请重新设置！")
                print("[ 轮询任务 ] 服务器重启时间 restart_interval 必须大于等于1分钟，请重新设置！")
                time.sleep(3)
                exit(0)

            # 启动程序前检查, 如果存在服务端则不再进行启动操作,改为每次循环结尾关闭进程
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq PalServer.exe'], capture_output=True, text=True)
            if 'PalServer.exe' not in result.stdout:
                INFO.logger.info("[ 轮询任务 ] 正在启动程序......")
                print("[ 轮询任务 ] 正在启动程序......")
                program_args = [self.conf['program_path']]
                if self.conf['arguments']:
                    INFO.logger.info("[ 轮询任务 ] 已配置额外参数")
                    print("[ 轮询任务 ] 已配置额外参数")
                    program_args.extend(self.conf['arguments'].split())
                if self.conf['use_multicore_options']:
                    INFO.logger.info("[ 轮询任务 ] 已开启多核选项")
                    print("[ 轮询任务 ] 已开启多核选项")
                    program_args.extend(["-useperfthreads", "-NoAsyncLoadingThread", "-UseMultithreadForDS"])
                print("[ 轮询任务 ] 启动参数：", self.conf['arguments'].split())
                subprocess.Popen(program_args)

            INFO.logger.info(f'[ 轮询任务 ] 服务器将进入重启倒计时，设置时长为 {self.conf["restart_interval"]} 秒......')
            print(f'[ 轮询任务 ] 服务器将进入重启倒计时，设置时长为 {self.conf["restart_interval"]} 秒......')
            
            # 如果设置了检查内存使用情况memory_monitor_enabled
            if self.conf['memory_monitor_enabled']:
                print("[ 内存监控 ] 已开启内存监控，将在内存使用超过阈值时重启程序......")
                
            # 服务器持续运行时间(重启间隔)
            for i in range(int(self.conf['restart_interval']), 0, -1):
                if self.conf['memory_monitor_enabled']:
                    if self.conf['polling_interval_seconds'] > 5:
                        # 检查内存使用情况
                        mem_info = psutil.virtual_memory()
                        mem_usage = mem_info.percent  # 获取内存使用百分比
                        # 如果内存使用超过阈值，则跳出倒计时，进行重启操作
                        if mem_usage > self.conf['memory_usage_threshold']:
                            print(f"[ 内存监控 ] 内存使用超过{self.conf['memory_usage_threshold']}%，正在重启程序......")
                            break
                    else:
                        INFO.logger.error("[ 内存监控 ] 轮询间隔 polling_interval_seconds 必须大于等于5秒，请重新设置！")
                        print("[ 内存监控 ] 轮询间隔 polling_interval_seconds 必须大于5秒，请重新设置！")
                        time.sleep(3)
                        exit(0)
                
                print(f'\r[ 轮询任务 ] 服务器将在 {i} 秒后重启......', end='')

                # 还剩30秒的时候发送rcon关服消息提醒
                if str(i) in self.conf['shutdown_notices'] and self.conf['rcon_enabled']:  # 检查是否有对应的通知
                    if self.conf['rcon_command']:
                        INFO.logger.info("RCON指令 {0}，正在发送关服通知......".format(self.conf['rcon_command']))
                        print("\r\033[K", end='')
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
                            
                print(f'\r[ 轮询任务 ] 服务器将在 {i} 秒后重启......', end='')
                time.sleep(1)
            # 关闭服务端 放在循环的结尾,可以让用户不用关闭服务器的情况下启动本脚本
            INFO.logger.info("[ 轮询任务 ] 正在关闭任何在运行的 PalServer 服务......")
            print("\r\033[K", end='')
            print("[ 轮询任务 ] 正在关闭任何在运行的 PalServer 服务......")
            subprocess.run(['taskkill', '/f', '/im', self.appName], stderr=subprocess.DEVNULL)


    def start_daemon(self):
        # 守护进程代码
        while True:
            try:
                # 检查服务是否在运行
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq PalServer.exe'], capture_output=True, text=True)
                if 'PalServer.exe' not in result.stdout:
                    print("\r\033[K", end='')
                    print('[ 守护进程 ] 监控到 PalServer 已停止,正在启动!!!')

                    # 启动程序
                    program_args = [self.conf['program_path']]
                    if self.conf['arguments']:
                        print("[ 守护进程 ] 已配置额外参数")
                        program_args.extend(self.conf['arguments'].split())
                    if self.conf['use_multicore_options']:
                        print("[ 守护进程 ] 已开启多核选项")
                        program_args.extend(["-useperfthreads", "-NoAsyncLoadingThread", "-UseMultithreadForDS"])
                    print("[ 守护进程 ] 启动参数：", self.conf['arguments'].split())
                    subprocess.Popen(program_args)
                        
                else:
                    print("\r\033[K", end='')
                    print('[ 守护进程 ] 监控到 PalServer 正在运行中,无需任何操作')
                # 倒数计时
                for i in range(int(self.conf['daemon_time']), 0, -1):
                    print("[ 守护进程 ] 将在 {0} 秒后进行下次检测".format(i), end='')
                    time.sleep(1)
            # 只有异常退出才会触发，手动关闭进程不会触发
            except Exception as e:
                INFO.logger.error(f"[ 守护进程 ] 程序异常终止，错误信息：{e}\n正在尝试重启程序......")
                print("\r\033[K", end='')
                print(f"[ 守护进程 ] 程序异常终止，错误信息：{e}\n正在尝试重启程序......")
                continue
            
def main():
    Task = TaskScheduler()

    polling_thread = threading.Thread(target=Task.polling_task)
    INFO.logger.info("[ 轮询任务 ] 已启动,每隔{0}秒重启 PalServer 进程......".format(Task.conf['restart_interval']))
    print("[ 轮询任务 ] 已启动,每隔{0}秒重启 PalServer 进程......".format(Task.conf['restart_interval']))
    polling_thread.start()
    time.sleep(1)
    # [ 轮询任务 ] 必须在最初启动 防止[ 轮询任务 ] kill掉[ 守护进程 ] 刚启动的服务端
    if Task.conf['daemon_enabled']:
        print("\r\033[K", end='')
        print("[ 守护进程 ] 已配置,在 5 秒后监控 PalServer 进程")
        time.sleep(5)  # 再延迟5秒 避免脚本启动时双开服务端。尽量避免10结尾以免和[ 轮询任务 ] 倒计时同时结束
        INFO.logger.info("[ 守护进程 ] 已启动,每隔{0}秒检测 PalServer 进程......".format(Task.conf['daemon_time']))
        print("\r\033[K", end='')
        print("[ 守护进程 ] 已启动,每隔{0}秒检测 PalServer 进程......".format(Task.conf['daemon_time']))
        daemon_thread = threading.Thread(target=Task.start_daemon)
        daemon_thread.start()

    polling_thread.join()
    if Task.conf['daemon_enabled']:
        daemon_thread.join()


if __name__ == '__main__':
    main()
