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

    # 打包成功后放入dist文件夹，如果已存在则覆盖
    if os.path.exists('dist/palworld-python-script.zip'):
        os.remove('dist/palworld-python-script.zip')
    shutil.move('palworld-python-script.zip', 'dist')
    print("打包后的palworld-python-script.zip已放入dist文件夹！")


if __name__ == '__main__':
    package_scripts()

