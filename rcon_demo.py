#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import configparser
import codecs
from rcon.battleye import Client
from rcon.battleye.proto import ServerMessage

# 读取配置文件
config = configparser.ConfigParser()
with codecs.open('config.ini', 'r', encoding='utf-8-sig') as f:
    config.read_file(f)
host = config.get('RCON', 'HOST')
port = config.getint('RCON', 'PORT')
password = config.get('RCON', 'AdminPassword')
command = config.get('RCON', 'COMMAND')


def my_message_handler(server_message: ServerMessage) -> None:
    """打印消息信息"""

    print('Server message:', server_message)


with Client(
        host,
        port,
        passwd=password,
        message_handler=my_message_handler
) as client:
    response = client.run('some_command', 'with', 'some', 'arguments')

print('Response:', response)
