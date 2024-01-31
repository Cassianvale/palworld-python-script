#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import rcon
from rcon.source.proto import Packet
from rcon.source import Client
from utils.log_control import INFO


class RconPatch:
    def __init__(self, rcon_host, rcon_port, rcon_password):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

    # 取消id校验，忽略SessionTimeout异常
    def patched_run(self, command: str, *args: str, encoding: str = "utf-8") -> str:
        """Patched run method that ignores SessionTimeout exceptions."""
        request = Packet.make_command(command, *args, encoding=encoding)
        response = self.communicate(request)

        return response.payload.decode(encoding)

    Client.run = patched_run

    def send_command(self, command):
        try:
            with Client(host=self.rcon_host,
                        port=self.rcon_port,
                        passwd=self.rcon_password,
                        timeout=1) as client:
                response = client.run(command)
            return True, response
        except rcon.exceptions.WrongPassword:
            INFO.logger.warning("[ RCON ] RCON密码错误,请检查相关设置")
            return False, "[ RCON ] RCON密码错误,请检查相关设置"
        except rcon.exceptions.EmptyResponse:
            INFO.logger.warning("[ RCON ] 服务器响应为空")
            return False, "[ RCON ] 服务器响应为空"
        except rcon.exceptions.UserAbort:
            INFO.logger.warning("[RCON] 用户中断")
            return False, "[RCON] 用户中断"
        except TimeoutError:
            INFO.logger.warning("[ RCON ] 正在检测RCON连接，请不要关闭......")
            return False, "[ RCON ] 正在检测RCON连接，请不要关闭......"
        except ConnectionResetError:
            INFO.logger.warning("[ RCON ] 连接已被远程主机关闭，请重新连接RCON")
            return False, "[ RCON ] 连接已被远程主机关闭，请重新连接RCON"
        except ConnectionRefusedError:
            INFO.logger.warning("[ RCON ] 连接已被远程主机拒绝")
            return False, "[ RCON ] 连接已被远程主机拒绝"
        except:
            INFO.logger.warning("[ RCON ] 未知错误，请联系开发人员")
            return False, "[ RCON ] 未知错误，请联系开发人员"
