# palworld-python-script

_✨ Suitable for palworld windows polling auto-restart server and auto-send shutdown notifications ✨_

[简体中文](./README.md) / English  

## Main Features  

1. Polling task to restart the server  
2. Send shutdown countdown via RCON commands before server restart  
3. Customize the backup time of the archive  

## Development Plan  

- [x] Added custom startup parameters for multi-core  
- [x] Customized shutdown notifications  
- [x] Added daemon process  
- [x] Converted rcon-cli client to third-party rcon library  
- [x] Memory usage percentage check  

## Usage  

1. Ensure that you have Python environment version 3.8 or higher installed.  
2. Run the command `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` to install the dependencies.  
3. Run the Python script `pyinstaller.py` to package `backup.exe`, `task_scheduler.exe`, and `config.ini`.  
4. Configure `config.ini` and run it in the same directory as the exe program.  
For specific usage, please refer to the Feishu document  
https://cxqzok4p36.feishu.cn/docx/YxPtdYoqCo5PdfxSyNgcDfIwnwe  

## Thanks  
rcon  
https://github.com/conqp/rcon  