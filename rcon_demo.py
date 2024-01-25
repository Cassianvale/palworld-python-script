#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from rcon.battleye import Client
from rcon.battleye.proto import ServerMessage


def my_message_handler(server_message: ServerMessage) -> None:
    """打印服务信息"""

    print('Server message:', server_message)


with Client(
        '192.168.0.1',
        65535,
        passwd='qwe123',
        message_handler=my_message_handler
) as client:
    response = client.run('some_command', 'with', 'some', 'arguments')

print('Response:', response)