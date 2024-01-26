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

## 使用方法

1.确保你安装了 Python 环境版本 3.8 或更高版本
2.执行命令安装依赖 `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
3.运行python脚本 `pyinstaller.py` 打包 `backup.exe`, `task_scheduler.exe`, `config.ini`
2.配置 `config.ini` 与exe程序同目录运行

具体使用请参考飞书文档
https://cxqzok4p36.feishu.cn/docx/YxPtdYoqCo5PdfxSyNgcDfIwnwe

## 感谢
rcon
https://github.com/conqp/rcon