# palworld-python-script

_✨ 适用于palworld windows轮询自动重启服务端自动发送关服通知 ✨_

简体中文 / [English](./README_EN.md)

## 主要功能

1.轮询任务重启服务端  
2.重启服务端前通过RCON指令发送关服倒计时  
3.自定义存档备份时间  

- backup.exe只有备份功能  
- task_scheduler.exe为定时轮询重启任务和关服倒计时 ， 可以选择是否开启关服倒计时，选择True的话就需要下载icon-cli客户端进行连接(后面直接改成调库，现在这样太傻了)  

## 开发计划
- [ ] 增加多核自定义启动参数
- [ ] 自定义关服通知
- [ ] 增加守护进程
- [ ] rcon-cli客户端转为第三方rcon库


## 使用方法

1.`pyinstaller --onefile task_scheduler.py`打包成exe文件  
2.配置`config.ini`与`task_scheduler.exe`同目录运行  
具体使用请参考飞书文档  
https://cxqzok4p36.feishu.cn/docx/YxPtdYoqCo5PdfxSyNgcDfIwnwe

## Thanks
rcon-cli客户端
https://github.com/gorcon/rcon-cli