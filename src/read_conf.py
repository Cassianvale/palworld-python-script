#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import configparser
import json
import os


def read_config():
    # 读取配置文件
    config = configparser.ConfigParser()
    with codecs.open('config.ini', 'r', encoding='utf-8-sig') as f:
        config.read_file(f)
    main_directory = config.get('Settings', 'main_directory')
    arguments = config.get('Settings', 'arguments')
    palinject_enabled = config.getboolean('Messages', 'PalInject_enabled')
    use_multicore_options = config.getboolean('Settings', 'use_multicore_options')
    restart_interval_hours = config.getint('Settings', 'restart_interval_hours')
    restart_interval_minutes = config.getint('Settings', 'restart_interval_minutes')
    daemon_enabled = config.getboolean('Settings', 'daemon_enabled')
    daemon_time = config.get('Settings', 'daemon_time')
    memory_monitor_enabled = config.getboolean('Memory', 'memory_monitor_enabled')
    polling_interval_seconds = config.getint('Memory', 'polling_interval_seconds')
    memory_usage_threshold = config.getint('Memory', 'memory_usage_threshold')
    shutdown_notices = dict(item.split(':') for item in config.get('RCON', 'shutdown_notices', raw=True).split(';'))
    shutdown_notices_cn = dict(item.split(':') for item in config.get('RCON', 'shutdown_notices_cn', raw=True).split(';'))
    rcon_enabled = config.getboolean('RCON', 'rcon_enabled')
    rcon_host = config.get('RCON', 'HOST')
    rcon_port = config.getint('RCON', 'PORT')
    rcon_password = config.get('RCON', 'AdminPassword', raw=True)
    rcon_command = config.get('RCON', 'COMMAND')

    announcement_enabled = config.getboolean('Messages', 'announcement_enabled')
    announcement_time = config.getint('Messages', 'announcement_time')

    backup_dir = config.get('Backup', 'backup_dir')
    del_old_backup_days = config.getint('Backup', 'del_old_backup_days')
    backup_interval_hours = config.getint('Backup', 'backup_interval_hours')
    backup_interval_minutes = config.getint('Backup', 'backup_interval_minutes')

    # 获取公告消息
    announcement_messages = []
    for i in range(1, 11):  # 10个公告消息
        key = f'announcement_messages_{i}'
        if config.has_option('Messages', key):
            message = config.get('Messages', key, raw=True)
            announcement_messages.append(message)
        else:
            break

    # 将小时和分钟转换为秒
    restart_interval = (restart_interval_hours * 60 + restart_interval_minutes) * 60
    backup_interval = (backup_interval_hours * 60 + backup_interval_minutes) * 60

    return {
        'main_directory': main_directory,
        'arguments': arguments,
        'palinject_enabled': palinject_enabled,
        'use_multicore_options': use_multicore_options,
        'rcon_enabled': rcon_enabled,
        'rcon_host': rcon_host,
        'rcon_port': rcon_port,
        'rcon_password': rcon_password,
        'rcon_command': rcon_command,
        'backup_interval': backup_interval,
        'restart_interval': restart_interval,
        'shutdown_notices': shutdown_notices,
        'shutdown_notices_cn': shutdown_notices_cn,
        'daemon_enabled': daemon_enabled,
        'daemon_time': daemon_time,
        'memory_monitor_enabled': memory_monitor_enabled,
        'polling_interval_seconds': polling_interval_seconds,
        'memory_usage_threshold': memory_usage_threshold,
        'announcement_enabled': announcement_enabled,
        'announcement_time': announcement_time,
        'announcement_messages': announcement_messages,
        'backup_dir': backup_dir,
        'del_old_backup_days': del_old_backup_days,
    }


if __name__ == '__main__':
    config = read_config()
    print(json.dumps(config, indent=4))

