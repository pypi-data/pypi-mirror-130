"""
录像服务sdk
"""

from . import main

message_middware_config = {
    "host": "127.0.0.1",
    "port": 1884,
    "password": "eHIGH2014",
    "username": "admin"
}
http_config = {
    "ip": "http://127.0.0.1",
    "port": "80"
}
rpc_config = {
    "ip": "127.0.0.1",
    "port": 10000,
    "service_name": "test"
}
cm = main.CallMethod(
    mmc=main.MqttMessageMiddlewareClientImpl(),
    hc=main.PyHttpClientImpl(),
    rc=main.PwRpcClientImpl(),
    mmcc=main.MqttMessageMiddlewareClientConfig(**message_middware_config),
    hcc=main.HttpClientConfig(**http_config),
    rcc=main.RpcClientConfig(**rpc_config)
)


def login(username: str, password: str, http_api_version: str):
    """
    登录sdk接口
    :param username: 用户名
    :param password:    密码
    :param http_api_version: 版本号
    :return:
    """
    return cm.message_http(
        method="post",
        data={
            "username": username,
            "password": password,
            "http_api_version": http_api_version
        },
        uri="/EHCommon/admin/user/login"
    )


def query_start(data):
    cm.message_middleware_publish(r"gs/record/start/req", data=data)


# @staticmethod
# def query_check(data):
#     cm.message_middleware_publish("gs/record/check/req", data=data)

# @staticmethod
# def check(param=None):
#     return cm.rpc_client.call(
#         module="gs_camera_record",
#         ip="127.0.0.1",
#         port="12001",
#         service_name="DemoRPCServer",
#         func="start",
#         param=param)


def start(param=None):
    return cm.rpc_client.call(
        module="gs_camera_record",
        base_config=cm.rpc_client_config,
        func="start",
        param=param)


def test_subscribe(callback):
    cm.message_middleware_subscribe(topic=r"gs/record/start/res", callback=callback)
