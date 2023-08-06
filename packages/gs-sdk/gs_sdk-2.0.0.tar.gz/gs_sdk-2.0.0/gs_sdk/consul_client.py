# -*- coding: utf-8 -*-
import consul
import socket

from . import PWConfig


class HGConsul(object):
    ''' 注册相同的服务名不会报错而是会覆盖！查询相同的服务永远只会取第一个，不能用于分布式节点！
    '''
    def __init__(self, host, port):
        """
        初始化，连接consul服务器
        :param host: 服务器ip地址
        :param port: 服务器端口
        """
        self._consul = consul.Consul(host, port)

    def register_service(self, name, host=None, port=8500, tags=None) -> bool:
        """
        向agent注册服务,服务名本身不用唯一,服务id重复了不会报错而是会覆盖
        :param name:服务名称,因为该字段这里被用作id,所以在一台服务器上必须是唯一值
        :param host:服务的ip地址
        :param port:服务的端口
        :param tags:
        :return: bool
        """
        tags = tags or []
        if host is None:
            host = self.get_host_ip()
        # 注册服务
        return self._consul.agent.service.register(
            name=name,
            service_id=name,
            address=host,
            port=port,
            tags=tags,
            token=PWConfig.consul_token,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
            check=consul.Check().tcp(host, port, "5s", "30s", "30s"))

    def delete_register(self, name) -> bool:
        """
        从agent删除服务
        :param name: 服务名称实际是服务id
        :return: bool
        """
        return self._consul.agent.service.deregister(name)

    def register_discovery(self) -> list:
        """
        发现所有服务，原始返回值是以服务名为键，Tags为值的词典，此处返回服务名列表
        库返回值中的数字是什么意思？数据一定在[1]吗？
        :return:
        """
        return self._consul.catalog.services()[1].keys()

    def get_service(self, name):
        """
        根据服务id/服务名获得服务的ip地址和端口.
        :param name: 服务名称
        :return:
        """
        service = self._consul.catalog.service(name, token=PWConfig.consul_token)
        if not (service and service[1]):            
            return None, None
        '''
        (index, [
                    {
                        "Node": "foobar",
                        "ServiceAddress": "10.1.10.12",
                        "ServiceID": "redis",
                        "ServiceName": "redis",
                        "ServiceTags": null,
                        "ServicePort": 8000
                    }
                ])
        同一个name可能存在多个服务，默认只取第一个
        agent的查询取ID，catalog的查询取名字，因此这里可能存在多个服务（如果有其他服务节点）
        分布式会存在问题！
        '''
        return service[1][0]['ServiceAddress'], service[1][0]['ServicePort']

    @staticmethod
    def get_host_ip():
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


def register_service(service_name, port, ip=None):
    """
    服务注册
    :param service_name: 服务名称,因为该字段也被用作id,所以在一台服务器上具有唯一性
    :param port: 服务的端口
    :param ip: 服务的ip地址
    :return:
    """
    try:
        if service_name:
            consul_client = HGConsul(PWConfig.consul_ip, PWConfig.consul_port)
            consul_client.register_service(service_name, host=ip, port=port)
        return True
    except:        
        return False


def get_service(service_name):
    """
    获得服务的ip地址和端口.
    :param service_name: 服务名称
    :return:
    """
    try:
        consul_client = HGConsul(PWConfig.consul_ip, PWConfig.consul_port)
        return consul_client.get_service(service_name)
    except:
        return None, None


if __name__ == '__main__':
    # consul服务器的ip
    host = "192.168.13.76"  # host = "http://forthink.xin/"
    # consul服务器对外的端口 不能使用字符串格式！
    port = 8500
    consul_client = HGConsul(host, port)

    name = 'apple'
    res = consul_client.register_service(name, host='192.168.1.23', port=1884, tags=['frute'])
    print('register', res)

    host2 = "192.168.0.101"
    consul_client2 = HGConsul(host2, port)
    res = consul_client2.register_service(name, host='192.168.1.22', port=1884, tags=['frute'])
    print('register2', res)

    res = consul_client.register_discovery()
    print('getall', res)
    res = consul_client.get_service(name)
    print('find', res)

    check = consul.Check().tcp(host, port, "5s", "30s", "30s")
    print('check', check)

    res = consul_client.delete_register(name)
    print('deregister', res)
    res = consul_client2.delete_register(name)
    print('deregister2', res)