# -*- coding: utf-8 -*-
from httplib2 import Http
import time
from .consul_client import get_service

import json

import pickle


class ComputeProxy(object):
    SUBMITTASK_NONBLOCKED = "submitTaskNonBlocked"

    SUBMITTASK_BLOCKED = "submitTaskBlocked"

    GET_TASK_RESULT = "getTaskResult"

    task_result = {}

    def __init__(self, module=None, ip="localhost", port="8888", type="json", time_out=30, service_name=None):

        # 通过consul方式获取信息
        if service_name:
            service_ip, service_port = get_service(service_name)
            if service_ip and service_port:
                ip = service_ip
                port = service_port
        # print(ip,port)
        self.__module = module
        self.__ip = ip
        self.__port = str(port)
        self._type = type
        self._time_out = time_out

    def setTaskModule(self, module):
        self.__module = module

    def __getattr__(self, name):

        def submitTaskBlocked(*args):
            url = "http://" + self.__ip + ":" + self.__port + "/" + self.SUBMITTASK_BLOCKED
            if self._type == 'bin':
                return self.__buildSubmitRpcPackage(url, name, *args)
            else:
                return self.__buildSubmitRpcPackage(url, name, args)

        return submitTaskBlocked

    def submitNonTaskBlocked(self, item):
        self.__checkTaskArrayFormation(item)
        url = "http://" + self.__ip + ":" + self.__port + "/" + self.SUBMITTASK_NONBLOCKED
        return self.__buildSubmitRpcPackage(url, None, item)

    def __buildSubmitRpcPackage(self, url, method, paras):

        if (self.__module is None):
            raise AttributeError

        post_data = {}

        try:
            http = Http(timeout=self._time_out)
            if (method is not None):
                post_data['method'] = method

            post_data['params'] = paras
            post_data['module'] = self.__module

            if self._type == 'json':

                post_http_data = json.dumps(post_data)
                hearder, content = http.request(url, method="POST",
                                                headers={"Content-Type": "application/json"},
                                                body=post_http_data)
            elif self._type == 'bin':
                hearder, content = http.request(url, method="POST",
                                                headers={"content-type": "application/octet-stream",
                                                         "rpc-class": post_data['module'],
                                                         "rpc-method": post_data['method']},
                                                body=post_data['params'])

            elif self._type == 'pickle':
                post_http_data = pickle.dumps(post_data, 2)
                hearder, content = http.request(url, method="POST",
                                                headers={"Content-Type": "application/octet-stream"},
                                                body=post_http_data)

        except Exception as e:
            log_info = {}
            log_info['ip'] = self.__ip
            log_info['port'] = self.__port
            log_info['type'] = self._type
            log_info['time_out'] = self._time_out
            log_info['time'] = time.time()
            log_info['method'] = method
            log_info['params'] = paras
            log_info['module'] = self.__module
            log_info['err_msg'] = str(e)

            if log_info['err_msg'] == 'timed out':
                raise Exception("连接超时")
            else:
                raise Exception("无法建立到服务器的连接，请检查服务器是否启动，地址是否正确,错误信息：" + str(e))

        if (hearder["status"] == "500"):
            raise Exception("服务器内部错误")

        if (hearder["status"] == "404"):
            raise Exception("错误的请求路径")

        if (hearder["status"] != "200"):
            raise Exception("请求没能被正确处理,HTTP错误码 " + hearder["status"])

        try:
            content = json.loads(content)
        except Exception:
            raise TypeError("返回结果格式错误，无法转换为json对象")

        if (content["result"] == "error"):
            if (content["code"] == 32601):
                raise Exception("任务过程出现错误")
            elif (content["code"] == 32602):
                raise ValueError("数据格式错误")
            elif (content["code"] == 32000):
                raise Exception("服务器内部出现错误")
            else:
                raise Exception("任务出现未知错误")

        return content['data']

    def __buildGetTaskResultPackage(self, task_ids, url):

        post_data = []
        for i in task_ids:
            task_id = {}
            task_id['task_id'] = i
            post_data.append(task_id)
        post_json_data = json.dumps(post_data)
        http = Http()

        try:
            hearder, content = http.request(url, "POST", post_json_data)
        except Exception:
            raise Exception("无法建立到服务器的连接，请检查服务器是否启动，地址是否正确")

        if (hearder["status"] == "500"):
            raise Exception("服务器内部错误")

        if (hearder["status"] == "404"):
            raise Exception("错误的请求路径")

        if (hearder["status"] != "200"):
            raise Exception("请求没能被正确处理,HTTP错误码 " + hearder["status"])

        try:
            content = json.loads(content)
        except Exception:
            raise TypeError("返回结果格式错误，无法转换为json对象")

        if (content["result"] == "error"):
            if (content["code"] == 32601):
                raise Exception("任务过程出现错误")
            elif (content["code"] == 32602):
                raise ValueError("数据格式错误")
            elif (content["code"] == 32000):
                raise Exception("服务器内部出现错误")
            else:
                raise Exception("任务出现未知错误")

        return content['data']

    def isTaskNonBlockedResultReady(self, task_id):

        if (len(task_id) < 1):
            raise ValueError("数据格式错误，格式为[ task_id,task_id.... ]")

        url = "http://" + self.__ip + ":" + self.__port + "/" + self.GET_TASK_RESULT
        ret = self.__buildGetTaskResultPackage(task_id, url)

        return_data = []
        for i in ret:
            if i['result'] == 'ready':
                return_data.append(i['data'])
            else:
                return_data.append(False)
        return return_data

    def __checkTaskArrayFormation(self, value):
        if len(value) < 1:
            raise ValueError("提交异步任务的的数据格式错误，格式为[['job1',[args]],['job2',[args]]....]")
        for i in value:
            if len(i) != 2:
                raise ValueError("提交异步任务的的数据格式错误,格式为[['job1',[args]],['job2',[args]]....]")

    def getTaskNonBlockedResult(self, task_id):
        if self.task_result[task_id] is not None:
            result = self.task_result[task_id]
            del self.task_result[task_id]
            return result
        else:
            raise AttributeError()
