#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess
import shutil
import os

"""小心别把自己的config.ini打包进去"""


def remove_ds_store(dir):
    # 删除DS_Store
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file == '.DS_Store':
                os.remove(os.path.join(root, file))


def package_scripts():

    if os.path.exists('dist/palworld-python-script.zip'):
        os.remove('dist/palworld-python-script.zip')
        print('已删除原dist/palworld-python-script.zip')
    if os.path.exists('palworld-python-script.zip'):
        os.remove('palworld-python-script.zip')
        print('已删除原palworld-python-script.zip')

    scripts = ['src/task_scheduler.py', 'src/backup.py']
    print('正在打包:', scripts)

    for script in scripts:

        command = 'pyinstaller', '--onefile', script
        subprocess.run(command)

    shutil.copy('src/config.ini', 'dist')

    shutil.make_archive('palworld-python-script', 'zip', 'dist')
    print("palworld-python-script 打包成功！")

    shutil.move('palworld-python-script.zip', 'dist')
    print("打包后的palworld-python-script.zip已放入dist文件夹！")


if __name__ == '__main__':
    remove_ds_store('dist')
    package_scripts()

