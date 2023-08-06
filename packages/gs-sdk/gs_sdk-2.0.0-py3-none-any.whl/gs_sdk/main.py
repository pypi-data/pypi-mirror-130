# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import paho.mqtt.client as mqtt
import json
import requests

from .ComputeProxy import ComputeProxy
from .config import MqttMessageMiddlewareClientConfig
from .config import HttpClientConfig
from  .config import RpcClientConfig

class MessageMiddlewareClient(metaclass=ABCMeta):
    """
    消息中间件客户端
    """

    @abstractmethod
    def publish(self, topic, data, base_config: MqttMessageMiddlewareClientConfig):
        pass


class MqttMessageMiddlewareClientImpl(MessageMiddlewareClient):
    """
    MQTT客户端
    """
    def publish(self, topic, data, base_config: MqttMessageMiddlewareClientConfig):
        client = mqtt.Client()
        client.username_pw_set(base_config.username, base_config.password)
        client.connect(base_config.host, base_config.port)
        if isinstance(data, str):
            data = data.encode("utf-8")
        elif isinstance(data, (list, dict, tuple, set)):
            data = json.dumps(data)
        else:
            raise TypeError("数据类型错误")
        client.publish(topic, data)

class HttpClient(metaclass=ABCMeta):
    """
    http客户端
    """
    @abstractmethod
    def call(self, base_config:HttpClientConfig, uri: str, data: json, method: str, headers=None):
        pass


class PyHttpClientImpl(HttpClient):
    """
    使用python包调用http接口
    """
    def call(self, base_config: HttpClientConfig, uri: str, data: json, method: str, headers=None):
        call_address = base_config.host + ":" + base_config.port + "/" + uri

        response = requests.request(method=method, url=call_address, json=data, headers=headers)
        return response.json()


class RpcClient(metaclass=ABCMeta):
    @abstractmethod
    def call(self, module=None, base_config: RpcClientConfig=None, func=None, param=None):
        pass


class PwRpcClientImpl(RpcClient):
    def call(self, module=None, base_config: RpcClientConfig=None, func=None, param=None):
        client = ComputeProxy(module=module,
                              ip=base_config.ip,
                              port=base_config.port,
                              service_name=base_config.service_name
                              )
        if hasattr(client, func):
            if isinstance(param, tuple):
                return getattr(client, func)(*param)
            elif isinstance(param, dict):
                return getattr(client, func)(param)
        raise Exception


class CallMethod:
    def __init__(self, mmc: MessageMiddlewareClient = None, hc: HttpClient = None, rc: RpcClient = None,
                 mmcc: MqttMessageMiddlewareClientConfig = None, hcc: HttpClientConfig = None,
                 rcc: RpcClientConfig =None
                 ):
        """
        初始化
        :param mmc: 消息中间件客户端
        :param hc: http客户端
        :param rc: rpc客户端
        :param mmcc: 消息中间件客户端配置如地址，端口等配置
        """
        self._middleware_client = mmc
        self._http_client = hc
        self._rc = rc
        self._middleware_client_config = mmcc
        self._http_client_config = hcc
        self._rpc_client_config = rcc

    @property
    def http_client_config(self):
        """
        获取http基础配置
        :return:
        """
        return self._http_client_config

    @http_client_config.setter
    def http_client_config(self, hcc: HttpClientConfig):
        """
        设置http基础配置
        :param hcc:
        :return:
        """
        self._http_client_config = hcc

    @property
    def message_middleware_client(self):
        """
        返回消息中间件客户端
        :return:
        """
        return self._middleware_client

    @message_middleware_client.setter
    def message_middleware_client(self, mmc: MessageMiddlewareClient):
        """
        设置消息中间件客户端
        :param mmc:
        :return:
        """
        self._middleware_client = mmc

    @property
    def http_client(self):
        """
        返回http客户端
        :return:
        """
        return self._http_client

    @http_client.setter
    def http_client(self, hc: HttpClient):
        """
        设置http客户端
        :param hc:
        :return:
        """
        self._http_client = hc

    @property
    def rpc_client(self):
        """
        获取rpc客户端
        :return:
        """
        return self._rc

    @rpc_client.setter
    def rpc_client(self, hc: RpcClient):
        """
        设置rpc客户端
        :param hc:
        :return:
        """
        self._rc = hc

    @property
    def message_middleware_client_config(self):
        """
        返回消息中间件配置
        :return:
        """
        return self._middleware_client_config

    @message_middleware_client_config.setter
    def message_middleware_client_config(self, mmcc: MqttMessageMiddlewareClientConfig):
        """
        动态设置消息中间件配置
        :param mmcc:
        :return:
        """
        self._middleware_client_config = mmcc

    @property
    def rpc_client_config(self):
        """
        获取rpc客户端配置
        :return:
        """
        return self._rpc_client_config

    @rpc_client_config.setter
    def rpc_client_config(self, rcc:RpcClientConfig):
        """
        设置rpc客户端配置
        :param rcc:
        :return:
        """
        self._rpc_client_config = rcc

    def message_middleware_publish(self, topic, data):
        """
        消息中间件发布主题
        :param topic:
        :param data:
        :return:
        """
        if not self._middleware_client:
            raise Exception("消息中间件客户端未初始化")

        if not hasattr(self._middleware_client, "publish"):
            raise Exception("消息中间件客户端未实现publish方法")
        self._middleware_client.publish(topic=topic, data=data, base_config=self._middleware_client_config)

    def message_http(self, method, data, uri, headers=None):
        """
        供sdk接口调用其他服务http接口
        :param method:
        :param data:
        :param url:
        :param headers:
        :return:
        """
        if not self._http_client:
            raise Exception("http客户端未初始化")

        if not hasattr(self._http_client, "call"):
            raise Exception("http客户端未实现call方法")

        return self._http_client.call(base_config=self._http_client_config, uri=uri, data=data, method=method, headers=headers)

    def message_rpc(self, module, func, param):
        """
        供sdk接口调用其他服务rpc接口
        :param module:
        :param ip:
        :param port:
        :param service_name:
        :param func:
        :param param:
        :return:
        """
        if not self._rc:
            raise Exception("rpc客户端未初始化")

        if not hasattr(self._rc, "call"):
            raise Exception("rpc客户端未实现call方法")

        return self._rc.call(module=module, base_config=self._rpc_client_config, func=func, param=param)

# message_middware_config = {
#     "host": "127.0.0.1",
#     "port": 1884,
#     "password": "eHIGH2014",
#     "username": "admin"
# }
# http_config = {
#     "ip": "http://127.0.0.1",
#     "port": "80"
# }
# rpc_config = {
#     "ip": "127.0.0.1",
#     "port": 10000,
#     "service_name": "test"
# }
# cm = CallMethod(
#     mmc=MqttMessageMiddlewareClientImpl(),
#     hc=PyHttpClientImpl(),
#     rc=PwRpcClientImpl(),
#     mmcc=MqttMessageMiddlewareClientConfig(**message_middware_config),
#     hcc= HttpClientConfig(**http_config),
#     rcc= RpcClientConfig(**rpc_config)
# )
