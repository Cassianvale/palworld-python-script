# palworld-python-script

_✨ 适用于palworld windows轮询自动重启服务端自动发送关服通知 ✨_

简体中文 / [English](./README_EN.md)

## 主要功能

1.轮询任务重启服务端  
2.重启服务端前通过RCON指令发送关服倒计时  
3.自定义存档备份时间  

- backup.exe
- task_scheduler.exe
- config.ini

## 开发计划

- [x] 增加多核自定义启动参数
- [x] 自定义关服通知
- [x] 增加守护进程
- [x] rcon-cli客户端转为第三方rcon库
- [x] 内存使用百分比检测

## 使用方法

1.`pyinstaller --onefile task_scheduler.py`打包成exe文件  
2.配置`config.ini`与`task_scheduler.exe`同目录运行  
具体使用请参考飞书文档  
https://cxqzok4p36.feishu.cn/docx/YxPtdYoqCo5PdfxSyNgcDfIwnwe

## 感谢
rcon
https://github.com/conqp/rcon