# _*_ coding: utf-8 _*_
import logging
from common.logger_tool.multiprocess_log_handler import MultiprocessHandler
import sys
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 定义日志输出格式
formattler = '%(asctime)s [%(threadName)s:%(thread)d-%(name)s] [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s'
fmt = logging.Formatter(formattler)

# 设置handleer日志处理器，日志具体怎么处理都在日志处理器里面定义
# SteamHandler 流处理器，输出到控制台,输出方式为stdout
#   StreamHandler默认输出到sys.stderr
# 设置handler所处理的日志级别。
#   只能处理 >= 所设置handler级别的日志
# 设置日志输出格式
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(fmt)

# 使用我们写的多进程版Handler理器，定义日志输出到mylog.log文件内
#   文件打开方式默认为 a
#   按分钟进行日志切割
log_name = "logger"
file_handler = MultiprocessHandler(log_name, when='D', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fmt)

# flask集成对logger增加handler日志处理器
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.info("this is a info log")

if __name__ == "__main__":
    import time

    for i in range(100):
        logger.info("test111111")
    print("打印完")
