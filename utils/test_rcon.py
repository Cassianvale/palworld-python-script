#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import codecs
import configparser



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
