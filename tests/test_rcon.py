#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from rcon.source.proto import Packet
from rcon.source import Client
from src.utils.log_control import INFO
from rcon.exceptions import WrongPassword, EmptyResponse, UserAbort


class TestRcon:
    def __init__(self, rcon_host, rcon_port, rcon_passwd):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.rcon_passwd = rcon_passwd

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
                        passwd=self.rcon_passwd,
                        timeout=1) as client:
                response = client.run(command)
            return True, response
        except WrongPassword:
            INFO.logger.warning("[ RCON ] RCON密码错误,请检查相关设置")
            return False, "[ RCON ] RCON密码错误,请检查相关设置"
        except EmptyResponse:
            INFO.logger.warning("[ RCON ] 服务器响应为空")
            return False, "[ RCON ] 服务器响应为空"
        except UserAbort:
            INFO.logger.warning("[RCON] 用户中断")
            return False, "[RCON] 用户中断"
        except TimeoutError:
            INFO.logger.warning("[ RCON ] RCON连接超时")
            return False, "[ RCON ] RCON连接超时"
        except ConnectionResetError:
            INFO.logger.warning("[ RCON ] 连接已被远程主机关闭，请重新连接RCON")
            return False, "[ RCON ] 连接已被远程主机关闭，请重新连接RCON"
        except ConnectionRefusedError:
            INFO.logger.warning("[ RCON ] 连接已被远程主机拒绝")
            return False, "[ RCON ] 连接已被远程主机拒绝"
        except Exception as e:
            INFO.logger.warning(f"[ RCON ] 未知错误: {str(e)}")
            return False, f"[ RCON ] 未知错误: {str(e)}"


if __name__ == '__main__':
    rcon = TestRcon(
        rcon_host="127.0.0.1",
        rcon_port=25575,
        rcon_passwd="qr14"
    )
    result, response = rcon.send_command("ShowPlayers")
    print(result, response)
