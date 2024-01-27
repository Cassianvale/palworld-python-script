# palworld-python-script  

_✨ 适用于palworld windows轮询自动重启服务端自动发送关服通知 ✨_  

简体中文 / [English](./README_EN.md)  

## 主要功能  

1.轮询任务重启服务端  
2.重启服务端前通过RCON指令发送关服倒计时  
3.自定义存档备份时间  

## 开发计划  

- [x] 增加多核自定义启动参数  
- [x] 自定义关服通知  
- [x] 增加守护进程  
- [x] rcon-cli客户端转为第三方rcon库  
- [x] 内存使用百分比检测  

## 使用说明

1.下载 Releases 中最新的安装包
https://github.com/Cassianvale/palworld-python-script/releases
2.有两个exe程序，一个是`task_scheduler.exe`轮询重启守护进程等，一个是`backup.exe`独立的定时备份存档，必须与`config.ini`配置文件放在同一目录下运行
3.修改`config.ini`配置文件，配置文件中有详细的说明

## 二次开发  

1.确保你安装了 Python 环境版本 3.8 或更高版本  
2.执行命令安装依赖 `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`  
3.控制台运行python脚本 `python pyinstaller.py` 打包 `backup.exe`, `task_scheduler.exe`, `config.ini`  
2.配置 `config.ini` 与exe程序同目录运行  

具体使用请参考飞书文档  
https://cxqzok4p36.feishu.cn/docx/YxPtdYoqCo5PdfxSyNgcDfIwnwe  

## 感谢  
rcon  
https://github.com/conqp/rcon  