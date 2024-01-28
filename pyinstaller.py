#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess
import shutil
import os


def package_scripts():

    scripts = ['task_scheduler.py', 'backup.py']

    pyinstaller_path = shutil.which('pyinstaller')

    if pyinstaller_path is None:
        print('pyinstaller not found')
        return

    for script in scripts:
        print('打包', scripts)
        command = ['pyinstaller', '--onefile', script]
        subprocess.run(command)

    shutil.copy('config.ini', 'dist')

    if os.path.exists('palworld-python-script.zip'):
        os.remove('palworld-python-script.zip')

    shutil.make_archive('palworld-python-script', 'zip', 'dist')
    print("palworld-python-script 打包成功！")


if __name__ == '__main__':
    package_scripts()

