# -*- coding: utf-8 -*-
import os
import sys
# 项目需要配置：

# mqtt配置
MQTT_IP = 'localhost'
MQTT_PORT = 1884

# 这个是后面加的,为了兼容以前代码,没配置默认user：admin pw：admin123
MQTT_USER = 'admin'
MQTT_PASSWORD = 'eHIGH2014'

# mqtt心跳
MQTT_KEEP_ALIVE = 60

# 打包方式json和pickle（默认json）
MQTT_PKG_TYPE = 'json'

# redis配置
REDIS_IP = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'eHIGH2014'
REDIS_DB = 0

# 默认数据库连接
DB_CONFIG = {
    'user': 'root',
    'password': 'eHIGH2014',
    'host': '127.0.0.1',
    'port': 3306,
    'dbname': 'test',
    'dbcharset': 'utf8',
    'use_unicode': True,
    'throw_alarm': True
}
# pymysql一次查询太多会卡死进程这里限制在20000
MAX_FIND_NUM = 20000

# 框架特有配置：

# 框架从数据库读取配置(False关闭,True开启)
CONFIG_FLAG = False

# 框架同步配置文件数据库
PW_DB_CONFIG = {
    'user': 'root',
    'password': 'eHIGH2014',
    'host': '127.0.0.1',
    'port': 3306,
    'dbname': 'python_worker_config',
    'dbcharset': 'utf8',
    'use_unicode': False,
    'throw_alarm': True,
    'tb_name': 'tb_config'
}

# 心跳服务：mqtt配置
USE_HEART = False
HEART_MQTT_IP = 'localhost'
HEART_MQTT_PORT = 1884
HEART_MQTT_USER = 'admin'
HEART_MQTT_PASSWORD = 'eHIGH2014'
HEART_TOPIC_DEL_DIR = '/home/ehigh/work/PythonWorker/Worker/'
HEART_TOPIC_FIRST = '/PythonWorker'
# 心跳发送时间
HEART_TIME = 1


# rpc默认超时时间
RPC_TIME_OUT = 5
RPC_REDIS_IP = 'localhost'
RPC_REDIS_PORT = 6379
RPC_REDIS_PASSWORD = 'eHIGH2014'
RPC_REDIS_DB = 7
RPC_REDIS_LOG_KEY = "RPC_ERROR_LOG"
RPC_REDIS_LOG_MAX = 50000

# 框架选择
SELECT_EPOLL = True

# 框架python使用
PYTHON_PATH = sys.executable

# 连接udp服务器将标准输出传递到udp服务器
udp_server = ('127.0.0.1', 50000)
# 查询status状态临时通信使用端口
STATUS_PORT = 31500

# consul ip,port
consul_ip = 'localhost'
consul_port = 8500
consul_token = 'f6786d6b-1901-87e5-78c3-074f90fc8fc6'

# 日志是否输出到终端
log_to_console = True

# CMqtt问题退出循环时间
break_time = 5

# 是否启用事件循环统计
flag_log_select = False
