#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import codecs
import configparser
from rcon.source.proto import Packet
from rcon.source import Client


class TestRcon:

    def __init__(self):
        # 读取根目录的config.ini
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
        with codecs.open(config_path, 'r', encoding='utf-8-sig') as f:
            config = configparser.ConfigParser()
            config.read_file(f)
            self.host = config.get('RCON', 'HOST')
            self.port = config.getint('RCON', 'PORT')
            self.passwd = config.get('RCON', 'AdminPassword')

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
