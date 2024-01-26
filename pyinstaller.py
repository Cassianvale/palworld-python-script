#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import subprocess
import shutil


def package_scripts():
    scripts = ['task_scheduler.py', 'backup.py']

    for script in scripts:
        command = ['pyinstaller', '--onefile', script]
        subprocess.run(command)

    shutil.copy('config.ini', 'dist')
    if os.path.exists('palworld-python-script.zip'):
        os.remove('palworld-python-script.zip')
    shutil.make_archive('palworld-python-script', 'zip', 'dist')


if __name__ == '__main__':
    package_scripts()
