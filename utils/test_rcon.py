#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from rcon.source.proto import Packet
from rcon.source import Client
import read_conf


class TestRcon:

    def __init__(self):
        self.conf = read_conf.read_config()
        self.host = self.conf['rcon_host']
        self.port = self.conf['rcon_port']
        self.passwd = self.conf['rcon_password']

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

    def test_rcon(self):
        with Client(
                self.host,
                self.port,
                passwd=self.passwd,
                timeout=1
        ) as client:
            response = client.run('ShowPlayers')

        print('Response:', response)


if __name__ == '__main__':
    rcon = TestRcon()
    rcon.test_rcon()
