# palworld-python-script

_✨ Suitable for palworld windows polling auto-restart server and auto-send shutdown notifications ✨_

[简体中文](./README.md) / English

## Main Features

1. Polling task to restart the server
2. Send shutdown countdown via RCON commands before server restart
3. Customize the backup time of the archive

- backup.exe only  
- task_scheduler.exe  
- config.ini

## Development Plan

- [x] Added custom startup parameters for multi-core
- [x] Customized shutdown notifications
- [x] Added daemon process
- [x] Converted rcon-cli client to third-party rcon library
- [x] Memory usage percentage check

## Usage

1. Package `task_scheduler.py` into an exe file with `pyinstaller --onefile task_scheduler.py`
2. Run `config.ini` in the same directory as `task_scheduler.exe`
For specific usage, please refer to the Feishu document  
https://cxqzok4p36.feishu.cn/docx/YxPtdYoqCo5PdfxSyNgcDfIwnwe

## Thanks
rcon
https://github.com/conqp/rcon