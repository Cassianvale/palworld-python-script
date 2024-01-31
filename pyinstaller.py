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

    scripts = ['task_scheduler.py', 'backup.py']

    for script in scripts:
        print('打包', scripts)
        command = ['pyinstaller', '--onefile', script]
        subprocess.run(command)

    shutil.copy('config.ini', 'dist')

    if os.path.exists('dist/palworld-python-script-v0.1.4.zip'):
        os.remove('dist/palworld-python-script-v0.1.4.zip')

    if os.path.exists('palworld-python-script-v0.1.4.zip'):
        os.remove('palworld-python-script-v0.1.4.zip')

    shutil.make_archive('palworld-python-script', 'zip', 'dist')
    print("palworld-python-script 打包成功！")

    shutil.move('palworld-python-script-v0.1.4.zip', 'dist')
    print("打包后的palworld-python-script.zip已放入dist文件夹！")


if __name__ == '__main__':
    remove_ds_store('dist')
    package_scripts()

